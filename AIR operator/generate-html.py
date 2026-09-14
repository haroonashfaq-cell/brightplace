#!/usr/bin/env python3
"""
Stage 10: Converts stage-09 final-enriched markdown articles to production-ready HTML.
Saves as 10-[slug].html in each article's folder.

SEO checklist this generator covers:
  - Canonical URL (extracted from WebPage schema)
  - Open Graph: type, title, description, url, image placeholder, dates
  - Twitter Card: summary_large_image with title + description
  - JSON-LD schemas: FAQPage, Article, WebPage (all embedded in <head>)
  - Semantic HTML: <article>, .article-intro on first paragraph, <section class="faq-section">
  - Speakable spec classes: .article-intro, .faq-section
  - meta keywords from primary + secondary keywords
  - Last reviewed footer
  - All external links: target="_blank" rel="noopener"
  - No <ul>/<li> (Webflow RichText rule)
  - No <h1> duplication (single H1 from article title)
  - Word count in HTML comment for reference
  - hreflang for en-US
"""

import os
import re
import glob
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MONTH_NAMES = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December",
}


def parse_frontmatter(content):
    """Extract YAML frontmatter as a dict and return remaining content."""
    if not content.startswith("---"):
        return {}, content
    end = content.index("---", 3)
    fm_block = content[3:end].strip()
    body = content[end + 3:].strip()

    meta = {}
    for line in fm_block.split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            meta[key] = val
    return meta, body


def extract_json_ld_blocks(markdown_body):
    """Pull all ```json blocks that contain schema.org context."""
    blocks = re.findall(r"```json\s*\n(.*?)```", markdown_body, re.DOTALL)
    schemas = []
    for block in blocks:
        block = block.strip()
        if '"@context"' in block and "schema.org" in block:
            try:
                parsed = json.loads(block)
                schemas.append(parsed)
            except json.JSONDecodeError:
                pass
    return schemas


def get_canonical_url(schemas):
    """Extract canonical URL from WebPage schema if present."""
    for s in schemas:
        if s.get("@type") == "WebPage" and s.get("url"):
            return s["url"]
        if s.get("@type") == "Article":
            mep = s.get("mainEntityOfPage", {})
            if isinstance(mep, dict) and mep.get("@id"):
                return mep["@id"]
    return ""


def strip_schema_sections(markdown_body):
    """Remove the schema JSON-LD sections from the article body."""
    body = re.sub(
        r"\n## (?:FAQ|Article|WebPage) Schema \(JSON-LD\)\s*\n```json\s*\n.*?```",
        "",
        markdown_body,
        flags=re.DOTALL,
    )
    return body.strip()


def count_words(text):
    """Count words in plain text (strip HTML tags first)."""
    plain = re.sub(r"<[^>]+>", "", text)
    return len(plain.split())


def format_date_display(date_str):
    """Convert 2026-09-01 to 'September 1, 2026'."""
    try:
        dt = datetime.strptime(date_str.strip(), "%Y-%m-%d")
        return f"{MONTH_NAMES[dt.month]} {dt.day}, {dt.year}"
    except (ValueError, KeyError):
        return date_str


def md_to_html(md_text):
    """Convert markdown to semantic HTML without external dependencies."""
    html = md_text

    # Horizontal rules
    html = re.sub(r"^\s*---\s*$", "<hr>", html, flags=re.MULTILINE)

    # Headings (### before ## before #)
    html = re.sub(r"^### (.+)$", r"<h3>\1</h3>", html, flags=re.MULTILINE)
    html = re.sub(r"^## (.+)$", r"<h2>\1</h2>", html, flags=re.MULTILINE)
    html = re.sub(r"^# (.+)$", r"<h1>\1</h1>", html, flags=re.MULTILINE)

    # Bold + italic combos, then bold, then italic
    html = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", html)
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
    html = re.sub(r"\*(.+?)\*", r"<em>\1</em>", html)

    # Links — external get target="_blank" rel="noopener"
    html = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        r'<a href="\2" target="_blank" rel="noopener">\1</a>',
        html,
    )

    # Wrap lines into paragraphs, skip existing HTML block elements
    lines = html.split("\n")
    result = []
    first_para_done = False
    in_faq = False
    faq_opened = False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            result.append("")
            continue

        # Detect FAQ section start
        if stripped.startswith("<h2>") and "frequently asked question" in stripped.lower():
            in_faq = True
            if not faq_opened:
                result.append('<section class="faq-section" aria-label="Frequently Asked Questions">')
                faq_opened = True
            result.append(stripped)
            continue

        # Already an HTML block element
        if stripped.startswith(("<h1", "<h2", "<h3", "<hr", "<section", "</section", "<blockquote")):
            result.append(stripped)
            continue

        # Bullet points — convert to <p> with bold label (Webflow-safe)
        if stripped.startswith("- "):
            bullet_text = stripped[2:]
            result.append(f"<p>{bullet_text}</p>")
            continue

        # First content paragraph gets .article-intro class
        if not first_para_done and not stripped.startswith("<"):
            result.append(f'<p class="article-intro">{stripped}</p>')
            first_para_done = True
            continue

        result.append(f"<p>{stripped}</p>")

    # Close FAQ section if opened
    if faq_opened:
        result.append("</section>")

    return "\n".join(result)


def build_html(meta, body_html, schemas):
    """Build a complete, production-ready HTML document."""
    title = meta.get("title", "")
    seo_title = meta.get("seo_title", title)
    description = meta.get("meta_description", "")
    slug = meta.get("slug", "")
    date_published = meta.get("date_published", "")
    date_modified = meta.get("date_modified", date_published)
    last_reviewed = meta.get("last_reviewed", "")
    author = meta.get("author", "AIR Communities")
    primary_keyword = meta.get("primary_keyword", "")
    secondary_kw = meta.get("secondary_keywords", "")

    # Build keywords meta from primary + secondary
    keywords_list = [primary_keyword]
    if secondary_kw:
        # Parse the YAML array-like string
        kw_matches = re.findall(r'"([^"]+)"', secondary_kw)
        keywords_list.extend(kw_matches)
    keywords_str = ", ".join(k for k in keywords_list if k)

    # Extract canonical URL from schemas
    canonical_url = get_canonical_url(schemas)

    # Serialize schemas for embedding
    schema_tags = ""
    for s in schemas:
        schema_tags += f'    <script type="application/ld+json">\n{json.dumps(s, indent=2)}\n    </script>\n'

    # Word count for reference
    word_count = count_words(body_html)

    # Format dates for display
    pub_display = format_date_display(date_published)
    mod_display = format_date_display(date_modified)

    # Determine if dates differ
    updated_tag = ""
    if date_modified and date_modified.strip() != date_published.strip():
        updated_tag = f' &middot; <time datetime="{date_modified.strip()}">Updated {mod_display}</time>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- SEO Title (distinct from H1) -->
    <title>{seo_title}</title>

    <!-- Core SEO Meta -->
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords_str}">
    <meta name="author" content="{author}">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
    <link rel="canonical" href="{canonical_url}">
    <link rel="alternate" hreflang="en-US" href="{canonical_url}">

    <!-- Open Graph -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="{seo_title}">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:image" content=""><!-- TODO: Add featured image URL before publishing -->
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="628">
    <meta property="og:locale" content="en_US">
    <meta property="article:published_time" content="{date_published.strip()}">
    <meta property="article:modified_time" content="{date_modified.strip()}">
    <meta property="article:author" content="{author}">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{seo_title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content=""><!-- TODO: Add featured image URL before publishing -->

    <!-- JSON-LD Structured Data -->
{schema_tags}
    <style>
        *,*::before,*::after {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.75;
            color: #1a1a1a;
            max-width: 780px;
            margin: 0 auto;
            padding: 48px 24px;
            background: #ffffff;
            -webkit-font-smoothing: antialiased;
        }}

        article {{ position: relative; }}

        /* Article meta bar */
        .article-meta {{
            color: #6b7280;
            font-size: 0.875rem;
            margin-bottom: 32px;
            padding-bottom: 16px;
            border-bottom: 1px solid #e5e7eb;
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
            align-items: center;
        }}

        /* Headings */
        h1 {{
            font-size: 2.1rem;
            line-height: 1.2;
            margin-bottom: 24px;
            color: #0f172a;
            font-weight: 700;
            letter-spacing: -0.02em;
        }}
        h2 {{
            font-size: 1.5rem;
            line-height: 1.3;
            margin-top: 48px;
            margin-bottom: 16px;
            color: #0f172a;
            font-weight: 600;
        }}
        h3 {{
            font-size: 1.2rem;
            line-height: 1.4;
            margin-top: 32px;
            margin-bottom: 12px;
            color: #1e293b;
            font-weight: 600;
        }}

        /* Body text */
        p {{
            margin-bottom: 18px;
            font-size: 1.05rem;
            color: #374151;
        }}

        /* Article intro — AEO citability target */
        .article-intro {{
            font-size: 1.125rem;
            line-height: 1.8;
            color: #1a1a1a;
            margin-bottom: 24px;
        }}

        /* Links */
        a {{
            color: #2563eb;
            text-decoration: underline;
            text-decoration-thickness: 1px;
            text-underline-offset: 2px;
            transition: color 0.15s ease;
        }}
        a:hover {{
            color: #1d4ed8;
        }}

        /* Horizontal rules */
        hr {{
            border: none;
            border-top: 1px solid #e5e7eb;
            margin: 40px 0;
        }}

        strong {{ font-weight: 600; color: #1e293b; }}

        /* FAQ section */
        .faq-section {{
            margin-top: 48px;
            padding-top: 32px;
            border-top: 2px solid #e5e7eb;
        }}
        .faq-section h3 {{
            color: #0f172a;
            margin-top: 28px;
        }}
        .faq-section p {{
            color: #4b5563;
        }}

        /* Article footer */
        .article-footer {{
            margin-top: 48px;
            padding-top: 24px;
            border-top: 1px solid #e5e7eb;
            color: #9ca3af;
            font-size: 0.8rem;
        }}

        /* Responsive */
        @media (max-width: 640px) {{
            body {{ padding: 24px 16px; }}
            h1 {{ font-size: 1.75rem; }}
            h2 {{ font-size: 1.3rem; margin-top: 36px; }}
            h3 {{ font-size: 1.1rem; }}
        }}
    </style>
</head>
<body>
    <!-- Word count: {word_count} -->
    <article itemscope itemtype="https://schema.org/Article">
        <header>
            <div class="article-meta">
                <span>By <span itemprop="author">{author}</span></span>
                &middot;
                <time datetime="{date_published.strip()}" itemprop="datePublished">{pub_display}</time>
                {updated_tag}
            </div>
        </header>

        <div itemprop="articleBody">
{body_html}
        </div>

        <footer class="article-footer">
            <p>Last reviewed: {last_reviewed if last_reviewed else pub_display}</p>
            <meta itemprop="dateModified" content="{date_modified.strip()}">
        </footer>
    </article>
</body>
</html>"""


def process_file(filepath):
    """Process a single 09-*.md file into a 10-*.html file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    meta, body = parse_frontmatter(content)
    schemas = extract_json_ld_blocks(body)
    clean_body = strip_schema_sections(body)
    body_html = md_to_html(clean_body)
    full_html = build_html(meta, body_html, schemas)

    # Output filename: 10-[slug].html
    slug = meta.get("slug", os.path.basename(filepath).replace("09-", "").replace("-final-enriched.md", ""))
    out_dir = os.path.dirname(filepath)
    out_path = os.path.join(out_dir, f"10-{slug}.html")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    return out_path


def main():
    pattern = os.path.join(BASE_DIR, "**", "09-*-final-enriched.md")
    files = glob.glob(pattern, recursive=True)

    if not files:
        print("No stage-09 files found!")
        return

    print(f"Found {len(files)} stage-09 files. Generating HTML...\n")

    results = {}
    for filepath in sorted(files):
        try:
            out_path = process_file(filepath)
            rel = os.path.relpath(out_path, BASE_DIR)
            community = rel.split(os.sep)[0]
            if community not in results:
                results[community] = []
            results[community].append(os.path.basename(out_path))
            print(f"  OK: {rel}")
        except Exception as e:
            print(f"  FAIL: {filepath} — {e}")

    total = sum(len(v) for v in results.values())
    print(f"\nDone! Generated {total} HTML files across {len(results)} communities.")
    for community, files_list in sorted(results.items()):
        print(f"\n  {community} ({len(files_list)} files):")
        for f in files_list:
            print(f"    - {f}")


if __name__ == "__main__":
    main()
