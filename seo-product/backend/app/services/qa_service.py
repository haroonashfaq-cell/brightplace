import logging
import re
from datetime import datetime

from supabase import create_client

from app.config import get_settings
from app.services.research_service import _update_job

logger = logging.getLogger(__name__)

# Known broken internal URLs that should never be linked
BROKEN_URLS = [
    "/resources/studio-apartments",
    "/resources/pet-friendly-houses-for-rent",
    "/resources/1-bedroom-apartments-near-me",
    "/guides/studio-apartments",
]

BANNED_PHRASES = [
    "signal", "in today's", "it's important to note", "it's worth noting",
    "in conclusion", "without further ado", "at the end of the day",
    "in this article", "as we all know", "needless to say",
    "deep dive", "dive into", "navigate", "landscape", "unlock", "leverage",
    "whether you're", "from x to y", "it should be mentioned",
    "interestingly", "notably", "arguably", "hidden gem", "best-kept secret",
    "vibrant", "bustling", "thriving", "let's take a look at",
]

BANNED_SOURCES = [
    "apartments.com", "zillow.com", "trulia.com", "rent.com", "zumper.com",
    "apartmentlist.com", "hotpads.com", "rentcafe.com", "realtor.com",
    "forrent.com", "padmapper.com", "apartmentratings.com", "yelp.com",
    "niche.com", "areavibes.com", "crimegrade.org", "openigloo.com",
    "walkscore.com", "reddit.com", "city-data.com", "biggerpockets.com",
]

APPROVED_GOV_DOMAINS = [
    ".gov", ".edu", "hud.gov", "consumerfinance.gov", "ftc.gov",
    "irs.gov", "census.gov", "bls.gov",
]


def _get_supabase():
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_service_key)


async def run_qa(
    project_id: str,
    article_id: str,
    user_id: str,
) -> dict:
    """Run all 6 QA checks on an article."""
    sb = _get_supabase()

    article = (
        sb.table("articles")
        .select("*")
        .eq("id", article_id)
        .eq("project_id", project_id)
        .single()
        .execute()
    )
    if not article.data:
        raise ValueError("Article not found")

    article_data = article.data
    content_md = article_data.get("content_md", "")

    # Extract body only (exclude schema JSON-LD blocks)
    body_md = content_md
    for marker in ["## FAQ Schema", "## Article Schema", "## WebPage Schema"]:
        if marker in body_md:
            body_md = body_md.split(marker)[0]

    # Get brief for comparison
    brief = (
        sb.table("briefs")
        .select("*")
        .eq("id", article_data["brief_id"])
        .single()
        .execute()
    )
    brief_data = brief.data if brief.data else {}

    # Get keyword_id for job tracking
    keyword_id = None
    if brief_data:
        report = (
            sb.table("research_reports")
            .select("keyword_id")
            .eq("id", brief_data.get("research_report_id", ""))
            .execute()
        )
        if report.data:
            keyword_id = report.data[0]["keyword_id"]

    if keyword_id:
        _update_job(sb, project_id, keyword_id, "qa", "running")

    try:
        # Run all 6 checks
        checks = []
        checks.append(_check_brand_compliance(body_md))
        checks.append(_check_seo_structure(body_md, brief_data))
        checks.append(_check_content_quality(body_md, brief_data))
        checks.append(_check_math_verification(body_md))
        checks.append(_check_link_audit(body_md))
        checks.append(_check_infrastructure(content_md))  # infrastructure checks full doc

        # Calculate overall score
        passed = sum(1 for c in checks if c["passed"])
        total = len(checks)
        seo_score = int((passed / total) * 100)

        qa_report = {
            "checks": checks,
            "passed": passed,
            "total": total,
            "score": seo_score,
            "all_passed": passed == total,
        }

        # Update article
        status = "qa_passed" if qa_report["all_passed"] else "draft"
        sb.table("articles").update({
            "qa_report": qa_report,
            "seo_score": seo_score,
            "status": status,
            "updated_at": datetime.utcnow().isoformat(),
        }).eq("id", article_id).execute()

        if keyword_id:
            _update_job(sb, project_id, keyword_id, "qa", "done", {
                "score": seo_score,
                "all_passed": qa_report["all_passed"],
            })
            if qa_report["all_passed"]:
                sb.table("selected_keywords").update({"status": "qa_passed"}).eq("id", keyword_id).execute()

        return sb.table("articles").select("*").eq("id", article_id).single().execute().data

    except Exception as e:
        logger.error(f"QA failed for article {article_id}: {e}")
        if keyword_id:
            _update_job(sb, project_id, keyword_id, "qa", "failed", error=str(e))
        raise


# ============================================================
# QA Check 1: Brand Compliance
# ============================================================

def _check_brand_compliance(content: str) -> dict:
    issues = []
    suggestions = []

    # Check for uppercase "Brightplace" or "BrightPlace"
    if re.search(r'(?<!\w)[B]rightplace|BrightPlace|BRIGHTPLACE', content):
        issues.append("Brand name must be lowercase 'brightplace'")
        suggestions.append("Replace all instances with 'brightplace'")

    # Check for banned phrases
    content_lower = content.lower()
    for phrase in BANNED_PHRASES:
        if phrase.lower() in content_lower:
            issues.append(f"Banned phrase found: '{phrase}'")
            suggestions.append(f"Remove or rephrase: '{phrase}'")

    # Check for em dashes (unicode — or inline --, but not --- horizontal rules on their own line)
    has_em_dash = "\u2014" in content
    # Check for inline double hyphens (not markdown horizontal rules)
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped == "---" or stripped == "":
            continue  # skip horizontal rules
        if " -- " in stripped or stripped.endswith("--") or stripped.startswith("--"):
            has_em_dash = True
            break
    if has_em_dash:
        issues.append("Em dashes found (use commas or periods instead)")
        suggestions.append("Replace em dashes with commas, periods, or parentheses")

    # Check CTA format
    if "app.brightplace.ai" in content and "brightplace.ai" in content:
        # Check if both appear on the same line
        for line in content.split("\n"):
            if "app.brightplace.ai" in line and "brightplace.ai" in line.replace("app.brightplace.ai", ""):
                issues.append("CTA has both app.brightplace.ai and brightplace.ai on the same line")
                break

    return {
        "name": "Brand Compliance",
        "passed": len(issues) == 0,
        "issues": issues,
        "suggestions": suggestions,
    }


# ============================================================
# QA Check 2: SEO Structure
# ============================================================

def _check_seo_structure(content: str, brief: dict) -> dict:
    issues = []
    suggestions = []

    # Extract frontmatter
    frontmatter = _extract_frontmatter(content)

    # H1 != SEO title
    title = frontmatter.get("title", "")
    seo_title = frontmatter.get("seo_title", "")
    if title and seo_title and title.strip().lower() == seo_title.strip().lower():
        issues.append("H1 title and SEO title are identical (must differ)")
        suggestions.append("Make SEO title a variation with different wording")

    # Word count
    word_count = len(re.findall(r'\b\w+\b', content))
    target = brief.get("word_count_target", 2000)
    if word_count < target * 0.8:
        issues.append(f"Word count ({word_count}) is below 80% of target ({target})")
        suggestions.append(f"Add {target - word_count} more words to reach target")

    # Entity density
    entities = brief.get("entities", [])
    for entity in entities[:5]:
        count = content.lower().count(entity.lower())
        if count < 3:
            issues.append(f"Entity '{entity}' only mentioned {count} times (need 3-8)")
            suggestions.append(f"Add more natural mentions of '{entity}'")

    # Internal links count (match both relative /resources/ and full URL with /resources/)
    internal_links = re.findall(r'\[.*?\]\([^)]*?/resources/[^)]+\)', content)
    if len(internal_links) < 7:
        issues.append(f"Only {len(internal_links)} internal links (need 7+)")
        suggestions.append("Add more internal links to /resources/ pages")

    # H2 count
    h2s = re.findall(r'^## .+', content, re.MULTILINE)
    if len(h2s) < 4:
        issues.append(f"Only {len(h2s)} H2 headings (need at least 4)")

    return {
        "name": "SEO Structure",
        "passed": len(issues) == 0,
        "issues": issues,
        "suggestions": suggestions,
    }


# ============================================================
# QA Check 3: Content Quality
# ============================================================

def _check_content_quality(content: str, brief: dict) -> dict:
    issues = []
    suggestions = []

    # FAQ count - detect multiple formats
    faq_section = ""
    for marker in ["## Frequently Asked", "## FAQ"]:
        if marker in content:
            faq_section = content.split(marker, 1)[-1]
            # Stop at schema blocks
            for end in ["## FAQ Schema", "## Article Schema", "## WebPage Schema"]:
                if end in faq_section:
                    faq_section = faq_section.split(end)[0]
            break
    faq_questions = re.findall(r'^\*\*.*?\?\*\*|^### .*?\?|^####.*?\?', faq_section, re.MULTILINE)
    min_faqs = 6  # per content-writing-guidelines: 6-8
    if len(faq_questions) < min_faqs:
        issues.append(f"Only {len(faq_questions)} FAQs found (need {min_faqs}+)")
        suggestions.append("Add more FAQ pairs for better PAA coverage")

    # Featured snippet paragraph (check first content paragraph after frontmatter)
    lines = content.split("\n")
    first_paragraph = ""
    in_frontmatter = False
    past_h1 = False
    for line in lines:
        if line.strip() == "---":
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter:
            continue
        if line.startswith("# "):
            past_h1 = True
            continue
        if past_h1 and line.strip() and not line.startswith("#"):
            first_paragraph = line.strip()
            break

    if first_paragraph:
        snippet_words = len(first_paragraph.split())
        if snippet_words < 45 or snippet_words > 60:
            issues.append(f"Featured snippet paragraph is {snippet_words} words (target: 49-55)")
            suggestions.append("Adjust to 49-55 words for featured snippet optimization")

    # Date stamps on dollar figures
    # Find lines with dollar figures and check if any date stamp exists on that line
    unstamped_lines = 0
    for line in content.split("\n"):
        if "$" not in line:
            continue
        dollar_matches = re.findall(r'\$[\d,]+', line)
        if dollar_matches and "(as of" not in line.lower():
            unstamped_lines += 1
    if unstamped_lines > 0:
        issues.append(f"{unstamped_lines} lines with dollar figures missing date stamps")
        suggestions.append("Add '(as of Q3 2026)' after dollar figures on each line")

    # CTA count
    cta_count = content.lower().count("app.brightplace.ai") + content.lower().count("brightplace.ai/")
    if cta_count < 3:
        issues.append(f"Only {cta_count} CTAs found (need 3)")
        suggestions.append("Add CTAs: after first H2, mid-article, and end")

    return {
        "name": "Content Quality",
        "passed": len(issues) == 0,
        "issues": issues,
        "suggestions": suggestions,
    }


# ============================================================
# QA Check 4: Math Verification
# ============================================================

def _check_math_verification(content: str) -> dict:
    issues = []
    suggestions = []

    # Check for percentage calculations
    percentages = re.findall(r'(\d+(?:\.\d+)?)\s*%', content)

    # Check for basic math claims like "X per month" or "X per year"
    monthly_yearly = re.findall(
        r'\$?([\d,]+(?:\.\d{2})?)\s*(?:per|a|/)\s*month.*?\$?([\d,]+(?:\.\d{2})?)\s*(?:per|a|/)\s*year',
        content,
        re.IGNORECASE,
    )
    for monthly, yearly in monthly_yearly:
        try:
            m = float(monthly.replace(",", ""))
            y = float(yearly.replace(",", ""))
            expected_yearly = m * 12
            if abs(y - expected_yearly) > 1:
                issues.append(
                    f"Math mismatch: ${monthly}/month should be ${expected_yearly:,.2f}/year, not ${yearly}/year"
                )
        except ValueError:
            pass

    # Note: More complex math verification would require Claude
    if not issues:
        suggestions.append("Basic math checks passed. Manual review recommended for complex calculations.")

    return {
        "name": "Math Verification",
        "passed": len(issues) == 0,
        "issues": issues,
        "suggestions": suggestions,
    }


# ============================================================
# QA Check 5: Link Audit
# ============================================================

def _check_link_audit(content: str) -> dict:
    issues = []
    suggestions = []

    # Extract all links
    links = re.findall(r'\[.*?\]\((.*?)\)', content)

    for url in links:
        # Check against known broken URLs
        for broken in BROKEN_URLS:
            if broken in url:
                issues.append(f"Broken URL detected: {url}")
                suggestions.append(f"Remove or replace link to {url}")

        # Check internal links use /resources/
        if url.startswith("/"):
            if not url.startswith("/resources/"):
                issues.append(f"Internal link uses wrong path: {url} (should use /resources/)")
                suggestions.append(f"Change to /resources/ prefix: {url}")

        # Check external links
        if url.startswith("http") and "brightplace" not in url:
            # Check banned sources
            is_banned = any(src in url.lower() for src in BANNED_SOURCES)
            if is_banned:
                issues.append(f"Banned source linked: {url}")
                suggestions.append(f"Remove link to banned source: {url}")
            else:
                is_approved = any(domain in url for domain in APPROVED_GOV_DOMAINS)
                if not is_approved:
                    issues.append(f"External link needs verification: {url}")
                    suggestions.append(f"Verify external link is still active: {url}")

    # Check for bare URLs (not in markdown link format), skip JSON-LD blocks
    body_for_bare = content.split("## FAQ Schema")[0] if "## FAQ Schema" in content else content
    bare_urls = re.findall(r'(?<!\()(https?://[^\s\)\"]+)(?!\))', body_for_bare)
    for url in bare_urls:
        if "brightplace" not in url and "schema.org" not in url:
            issues.append(f"Bare URL found (should be markdown link): {url}")

    return {
        "name": "Link Audit",
        "passed": len(issues) == 0,
        "issues": issues,
        "suggestions": suggestions,
    }


# ============================================================
# QA Check 6: Infrastructure
# ============================================================

def _check_infrastructure(content: str) -> dict:
    issues = []
    suggestions = []

    # Check for http:// (should be https://)
    http_links = re.findall(r'http://(?!localhost)', content)
    if http_links:
        issues.append(f"{len(http_links)} insecure http:// links found")
        suggestions.append("Change all http:// to https://")

    # Check for legacy paths
    if "/knowledgebase/" in content:
        issues.append("Legacy /knowledgebase/ path found (use /resources/)")
        suggestions.append("Replace all /knowledgebase/ with /resources/")

    if "/guides/" in content:
        issues.append("Legacy /guides/ path found (use /resources/)")
        suggestions.append("Replace all /guides/ with /resources/")

    # Check frontmatter exists (may be wrapped in ```markdown fence)
    stripped = content.strip()
    if stripped.startswith("```"):
        stripped = stripped.split("\n", 1)[1] if "\n" in stripped else stripped
    if not stripped.strip().startswith("---"):
        issues.append("Missing YAML frontmatter")
        suggestions.append("Add frontmatter with title, seo_title, meta_description, slug, date")
    else:
        frontmatter = _extract_frontmatter(content)
        required = ["title", "seo_title", "meta_description", "slug"]
        for field in required:
            if field not in frontmatter:
                issues.append(f"Missing frontmatter field: {field}")

    # Check no H1 in body (after frontmatter)
    body = content
    if "---" in content:
        parts = content.split("---")
        if len(parts) >= 3:
            body = "---".join(parts[2:])
    h1_in_body = re.findall(r'^# [^#]', body, re.MULTILINE)
    if len(h1_in_body) > 1:
        issues.append(f"Multiple H1 tags found in body ({len(h1_in_body)})")
        suggestions.append("Keep only one H1 at the top, use H2+ for sections")

    # Check for markdown tables (should use bullet points)
    if re.search(r'\|.*\|.*\|', content):
        issues.append("Markdown table found (use bold-label bullet points instead)")
        suggestions.append("Convert table to bullet point format: **Label:** value")

    return {
        "name": "Infrastructure",
        "passed": len(issues) == 0,
        "issues": issues,
        "suggestions": suggestions,
    }


# ============================================================
# Helpers
# ============================================================

def _extract_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown content."""
    # Strip markdown code fence if present
    text = content.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text

    if not text.strip().startswith("---"):
        return {}

    parts = text.split("---")
    if len(parts) < 3:
        return {}

    frontmatter = {}
    for line in parts[1].strip().split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            frontmatter[key.strip()] = value.strip().strip('"').strip("'")

    return frontmatter
