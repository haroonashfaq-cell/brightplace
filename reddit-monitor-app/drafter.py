"""AI Draft Engine — uses Claude to draft Reddit answers."""
import re
import random
import anthropic
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL, MAX_TOKENS, TEMPERATURE
from database import get_articles, get_setting


def find_best_article(text):
    """Find the best matching brightplace article for a post."""
    articles = get_articles()
    text_lower = text.lower()

    best_match = None
    best_score = 0

    for art in articles:
        keywords = [k.strip() for k in art["keywords"].split(",") if k.strip()]
        score = 0
        for kw in keywords:
            if kw.lower() in text_lower:
                score += 1

        if score > best_score:
            best_score = score
            best_match = art

    return best_match if best_score > 0 else None


def should_be_promotional():
    """Decide if this answer should include a link based on promotional ratio."""
    ratio = float(get_setting("promotional_ratio", "0.20"))
    return random.random() < ratio


def draft_warmup_answer(post):
    """Draft a short karma-building comment for warmup subreddits.
    No links, no apartment content — just genuine engagement."""
    if not ANTHROPIC_API_KEY:
        return {
            "relevance": "HIGH",
            "link_opportunity": "NONE",
            "suggested_link": "",
            "answer": "Error: ANTHROPIC_API_KEY not set",
            "is_promotional": False,
        }

    prompt = f"""Write a short Reddit comment reply to this post. You are building karma on a new account.

r/{post.get('subreddit', 'unknown')} post:
Title: {post['title']}
Body: {post.get('content', '(no body)')[:1000]}

RULES:
- 20-50 words MAX. Short and punchy.
- Be genuinely helpful, funny, or relatable
- All lowercase, casual, sound human
- NO links. NO mentions of apartments/renting/housing.
- Match the subreddit's vibe (funny for AskReddit, helpful for NoStupidQuestions, etc.)
- Use 0-1 Reddit slang (lol, tbh, ngl, fr)

Just write the comment. Nothing else. No labels, no formatting."""

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=100,
            temperature=0.95,
            system="You write extremely short, casual Reddit comments to build karma. 20-50 words max. Sound like a real person. No formatting.",
            messages=[{"role": "user", "content": prompt}],
        )
        answer = response.content[0].text.strip()
        # Strip any markdown
        answer = re.sub(r'\*\*([^*]+)\*\*', r'\1', answer)
        answer = re.sub(r'\*([^*]+)\*', r'\1', answer)

        return {
            "relevance": "HIGH",
            "link_opportunity": "NONE",
            "suggested_link": "",
            "answer": f"[WARMUP] {answer}",
            "is_promotional": False,
        }
    except Exception as e:
        return {
            "relevance": "SKIP",
            "link_opportunity": "NONE",
            "suggested_link": "",
            "answer": f"Error: {str(e)}",
            "is_promotional": False,
        }


def draft_answer(post, force_link=False):
    """Use Claude to draft a Reddit answer for a post."""
    # Route warmup posts to separate drafter
    if post.get("tier") == "warmup":
        return draft_warmup_answer(post)

    if not ANTHROPIC_API_KEY:
        return {
            "relevance": "SKIP",
            "link_opportunity": "NONE",
            "suggested_link": "",
            "answer": "Error: ANTHROPIC_API_KEY not set",
            "is_promotional": False,
        }

    tone_profile = get_setting("tone_profile", "")
    text = f"{post['title']} {post.get('content', '')}"
    matched_article = find_best_article(text)
    is_promotional = force_link or (matched_article and should_be_promotional())

    article_context = ""
    if matched_article and is_promotional:
        article_context = f"\n\nA relevant article exists: {matched_article['title']} at {matched_article['url']}\nInclude this link at the END of your answer with casual framing."
    elif matched_article:
        article_context = f"\n\nA relevant article exists ({matched_article['title']}) but do NOT include a link in this answer. Just answer helpfully without any links."

    # Build article list for Claude
    articles = get_articles()
    article_list = "\n".join([f"- {a['title']}: {a['url']}" for a in articles])

    prompt = f"""{tone_profile}

---

r/{post.get('subreddit', 'unknown')} post:

Title: {post['title']}
Body: {post.get('content', '(no body)')[:1500]}
{article_context}

Available articles (only link ONE if instructed above):
{article_list}

Write a Reddit comment reply. STRICT RULES:
- 40-80 words MAX. Count them. Over 80 = fail.
- All lowercase, no formatting, no bold, no lists
- Sound like a real person typing fast on their phone
- One specific detail, one caveat, end with a question if natural
- If it reads like AI wrote it, start over

Respond in this EXACT format:

RELEVANCE: [HIGH/MEDIUM/LOW/SKIP]
LINK_OPPORTUNITY: [HIGH/MEDIUM/LOW/NONE]
SUGGESTED_LINK: [URL or NONE]

DRAFTED_ANSWER:
[your reply — 40-80 words, lowercase, no formatting]"""

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            system="You write extremely short Reddit comments. 40-80 words MAX. All lowercase, no markdown, no bold, no lists, no headers. You sound like a real person typing on their phone. If your drafted answer exceeds 80 words, you have failed.",
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text

        # Parse response
        result = {
            "relevance": "MEDIUM",
            "link_opportunity": "NONE",
            "suggested_link": "",
            "answer": "",
            "is_promotional": is_promotional,
        }

        for line in text.split("\n"):
            if line.startswith("RELEVANCE:"):
                result["relevance"] = line.split(":", 1)[1].strip()
            elif line.startswith("LINK_OPPORTUNITY:"):
                result["link_opportunity"] = line.split(":", 1)[1].strip()
            elif line.startswith("SUGGESTED_LINK:"):
                val = line.split(":", 1)[1].strip()
                if val != "NONE":
                    result["suggested_link"] = val

        if "DRAFTED_ANSWER:" in text:
            answer = text.split("DRAFTED_ANSWER:", 1)[1].strip()
        else:
            answer = text

        # Strip markdown formatting that AI loves to add
        answer = re.sub(r'\*\*([^*]+)\*\*', r'\1', answer)  # **bold**
        answer = re.sub(r'\*([^*]+)\*', r'\1', answer)      # *italic*
        answer = re.sub(r'^#+\s*', '', answer, flags=re.MULTILINE)  # headers
        answer = re.sub(r'^\s*[-*]\s+', '', answer, flags=re.MULTILINE)  # bullets
        answer = re.sub(r'^\s*\d+\.\s+', '', answer, flags=re.MULTILINE)  # numbered
        answer = re.sub(r'\n{2,}', ' ', answer)  # collapse paragraph breaks
        answer = answer.strip()

        result["answer"] = answer

        # If we have a matched article but Claude didn't suggest it, add it
        if matched_article and is_promotional and not result["suggested_link"]:
            result["suggested_link"] = matched_article["url"]

        return result

    except Exception as e:
        return {
            "relevance": "SKIP",
            "link_opportunity": "NONE",
            "suggested_link": "",
            "answer": f"Error: {str(e)}",
            "is_promotional": False,
        }
