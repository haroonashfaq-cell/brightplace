#!/usr/bin/env python3
"""
brightplace Reddit Answer Drafter

Takes a Reddit post (title + body) and drafts an expert answer
using Claude, with optional brightplace article link.

Usage:
  python reddit_answer_drafter.py "Post title here" "Post body here" "subreddit_name"
  python reddit_answer_drafter.py --interactive

Setup:
  pip install anthropic
  export ANTHROPIC_API_KEY=sk-ant-...
"""

import os
import sys
import re
import argparse

BRIGHTPLACE_ARTICLES = {
    # Guides
    "rent|afford|budget|cost|monthly|true cost": "https://www.brightplace.ai/guides/your-true-monthly-cost",
    "how to rent|first apartment|renting process|application": "https://www.brightplace.ai/guides/how-to-rent-an-apartment",
    "austin|atx|round rock|cedar park": "https://www.brightplace.ai/guides/austin-young-professionals",
    "brooklyn|williamsburg|park slope|bushwick": "https://www.brightplace.ai/guides/brooklyn-neighborhood-guide",
    "charlotte|university city|south end|noda": "https://www.brightplace.ai/guides/charlotte-affordable-neighborhoods",
    "chicago.*pet|chicago.*dog": "https://www.brightplace.ai/guides/chicago-pet-owners",
    "dallas|dfw|plano|frisco|mckinney": "https://www.brightplace.ai/guides/dallas-families",
    "denver|capitol hill|rino|highland": "https://www.brightplace.ai/guides/denver-city-orientation",
    "san diego.*dog|sd.*dog|dog.*san diego": "https://www.brightplace.ai/guides/dog-friendly-neighborhoods-san-diego",
    "houston|woodlands|sugar land": "https://www.brightplace.ai/guides/houston-city-orientation",
    "kansas city|kc metro": "https://www.brightplace.ai/guides/kansas-city-young-professionals",
    "nashville|music city": "https://www.brightplace.ai/guides/nashville-corporate-relocation-neighborhoods",
    "philadelphia|philly|manayunk|center city": "https://www.brightplace.ai/guides/philadelphia-city-orientation",
    "phoenix|scottsdale|chandler|gilbert|tempe": "https://www.brightplace.ai/guides/phoenix-renters-orientation",
    "salt lake|slc|utah": "https://www.brightplace.ai/guides/salt-lake-city-renters-orientation",
    "tampa|st pete": "https://www.brightplace.ai/guides/tampa-renters-orientation",
    # Resources
    "pet friendly|pet deposit|pet rent|breed restrict|dog friendly|cat friendly": "https://www.brightplace.ai/resources/pet-friendly-apartments-greenville-sc",
    "renters insurance|roommate.*insurance|insurance.*roommate": "https://www.brightplace.ai/resources/renters-insurance-with-roommates",
    "short.term lease|month to month|temporary lease|flexible lease": "https://www.brightplace.ai/resources/short-term-lease-agreement",
    "sublet|sublease|nyc.*sublet|subletting": "https://www.brightplace.ai/resources/sublet-apartments-nyc",
    "tour.*question|what to ask|apartment tour|touring": "https://www.brightplace.ai/resources/questions-to-ask-when-touring-an-apartment",
    "dog park|bark park": "https://www.brightplace.ai/resources/apartments-with-dog-parks",
    "attached garage|garage apartment|private garage": "https://www.brightplace.ai/resources/apartments-with-attached-garages",
    "nyc.*1 bedroom|nyc.*one bedroom|1br.*nyc|manhattan.*rent": "https://www.brightplace.ai/resources/one-bedroom-apartment-nyc",
    "mission beach|pacific beach|san diego.*rent": "https://www.brightplace.ai/resources/renting-mission-beach-san-diego",
    "no deposit|deposit alternative|waive deposit": "https://www.brightplace.ai/resources/homes-for-rent-no-deposit",
}


def find_best_article(text):
    """Find the best matching brightplace article."""
    text_lower = text.lower()
    for pattern, url in BRIGHTPLACE_ARTICLES.items():
        if re.search(pattern, text_lower):
            return url
    return None


def draft_answer(title, body, subreddit="unknown"):
    """Use Claude to draft a Reddit answer."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("\n❌ ANTHROPIC_API_KEY not set.")
        print("Run: export ANTHROPIC_API_KEY=sk-ant-your-key")
        sys.exit(1)

    suggested_article = find_best_article(f"{title} {body}")

    article_context = ""
    if suggested_article:
        article_context = f"\n\nA potentially relevant article exists at: {suggested_article}\nOnly include this link if it genuinely helps answer the question. Place it at the END of your answer."

    prompt = f"""You are a renter education expert. You sound like a real Reddit user who knows the apartment market well. You are NOT a brand or company representative.

A Reddit user posted in r/{subreddit}:

Title: {title}
Body: {body[:2000]}{article_context}

Draft a Reddit answer following these rules:
- 100-200 words maximum
- First sentence directly answers the question
- Include at least one specific number or dollar figure
- Sound like a real person on Reddit, NOT a company
- Do NOT say "brightplace" anywhere
- Be honest about tradeoffs and downsides
- If including a link, use casual framing at the END only:
  "There's a solid breakdown here: [URL]"
  "Someone put together a walkthrough that covers this: [URL]"
- Do NOT link if the article doesn't directly help
- Maximum ONE link

Also rate:
RELEVANCE: HIGH/MEDIUM/LOW/SKIP
LINK_OPPORTUNITY: HIGH/MEDIUM/LOW/NONE

Format your response EXACTLY like this:

RELEVANCE: [value]
LINK_OPPORTUNITY: [value]

ANSWER:
[your Reddit answer, ready to copy-paste]"""

    try:
        import requests
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1000,
                "temperature": 0.7,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["content"][0]["text"]

    except ImportError:
        print("❌ Missing dependency. Run: pip install requests")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Claude API error: {e}")
        sys.exit(1)


def interactive_mode():
    """Interactive mode: paste post details, get a draft."""
    print("\n" + "=" * 60)
    print("brightplace Reddit Answer Drafter")
    print("=" * 60)

    while True:
        print("\n--- New Post ---")
        subreddit = input("\nSubreddit (e.g., apartments): ").strip()
        if not subreddit:
            subreddit = "unknown"

        title = input("Post title: ").strip()
        if not title:
            print("No title entered. Exiting.")
            break

        print("Post body (paste text, then press Enter twice to submit):")
        body_lines = []
        empty_count = 0
        while True:
            line = input()
            if line == "":
                empty_count += 1
                if empty_count >= 2:
                    break
            else:
                empty_count = 0
                body_lines.append(line)
        body = "\n".join(body_lines)

        print("\n⏳ Drafting answer with Claude...\n")
        result = draft_answer(title, body, subreddit)

        print("=" * 60)
        print(result)
        print("=" * 60)

        # Check for matching article
        suggested = find_best_article(f"{title} {body}")
        if suggested:
            print(f"\n📎 Matching article: {suggested}")

        another = input("\nDraft another? (y/n): ").strip().lower()
        if another != "y":
            break

    print("\nDone.")


def main():
    parser = argparse.ArgumentParser(description="brightplace Reddit Answer Drafter")
    parser.add_argument("title", nargs="?", help="Reddit post title")
    parser.add_argument("body", nargs="?", default="", help="Reddit post body")
    parser.add_argument("subreddit", nargs="?", default="unknown", help="Subreddit name")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    args = parser.parse_args()

    if args.interactive or not args.title:
        interactive_mode()
    else:
        print("\n⏳ Drafting answer...\n")
        result = draft_answer(args.title, args.body, args.subreddit)
        print("=" * 60)
        print(result)
        print("=" * 60)

        suggested = find_best_article(f"{args.title} {args.body}")
        if suggested:
            print(f"\n📎 Matching article: {suggested}")


if __name__ == "__main__":
    main()
