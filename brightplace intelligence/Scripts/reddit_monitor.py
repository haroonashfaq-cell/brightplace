#!/usr/bin/env python3
"""
brightplace Reddit Monitor & Draft Agent

Monitors target subreddits for renter-relevant posts,
drafts expert answers using Claude, and sends opportunities to Slack.

Usage:
  python reddit_monitor.py              # Run once, check all subreddits
  python reddit_monitor.py --tier high  # Check only high-priority subs
  python reddit_monitor.py --dry-run    # Print results without sending to Slack

Setup:
  1. pip install anthropic requests feedparser
  2. Set environment variables:
     export ANTHROPIC_API_KEY=sk-ant-...
     export SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
  3. Run: python reddit_monitor.py

Scheduling:
  Add to crontab for automatic monitoring:
  */15 * * * * cd /path/to/Scripts && python reddit_monitor.py >> reddit_monitor.log 2>&1
"""

import os
import re
import json
import time
import hashlib
import argparse
from datetime import datetime, timedelta
from pathlib import Path

import feedparser
import requests

# --- CONFIGURATION ---

SUBREDDITS = {
    "high": [
        "ApartmentHunting", "renting", "personalfinance", "FirstTimeRenter", "Frugal"
    ],
    "city": [
        "AskNYC", "askdfw", "Denver", "Charlotte", "Austin", "phoenix",
        "Philadelphia", "nashville", "SanDiego", "houston", "Tampa",
        "Chicago", "Atlanta", "Seattle", "MinneapolisMN", "SaltLakeCity",
        "kansascity", "Columbus", "Knoxville", "raleigh"
    ],
    "topical": [
        "dogs", "RemoteWork", "RealEstate"
    ]
}

POSITIVE_KEYWORDS = [
    r"apartment hunt", r"finding an apartment", r"apartment search",
    r"how to find an apartment", r"apartment tour", r"touring apartment",
    r"what to ask", r"leasing office", r"leasing agent",
    r"move.in cost", r"move.in fee", r"security deposit",
    r"pet friendly", r"pet.friendly", r"pet deposit", r"pet rent",
    r"breed restriction", r"dog friendly", r"cat friendly",
    r"renters insurance", r"renter.s insurance", r"roommate insurance",
    r"sublet", r"subletting", r"sublease",
    r"short.term lease", r"month.to.month",
    r"lease break", r"break my lease", r"early termination",
    r"no credit check", r"bad credit apartment", r"second chance apartment",
    r"first apartment", r"first time renter",
    r"how much rent", r"afford rent", r"rent.to.income",
    r"30. rule", r"40x rule", r"rent budget", r"rent afford",
    r"cheap apartment", r"affordable apartment",
    r"under .1.000", r"under .1.500", r"under .2.000",
    r"one bedroom", r"1 bedroom", r"two bedroom", r"2 bedroom",
    r"studio apartment", r"furnished apartment",
    r"apartment with garage", r"attached garage",
    r"apartment dog park", r"apartment with pool",
    r"in.unit laundry", r"washer dryer",
    r"apartment parking", r"apartment amenities", r"apartment fees",
    r"application fee", r"broker fee", r"no.fee apartment",
    r"rent stabiliz", r"rent control",
    r"apartment scam", r"rental scam",
    r"moving to", r"relocating to", r"where should I live",
    r"neighborhood for", r"cost of living",
    r"apartment near", r"apartments in", r"renting in", r"rent in",
    r"looking for apartment", r"apartment advice",
    r"apartment question", r"apartment recommend",
    r"renters rights", r"tenant rights",
    r"security deposit return", r"utility cost", r"utilities included",
    r"apartment checklist", r"apartment vs", r"renting vs buying",
]

NEGATIVE_KEYWORDS = [
    r"eviction notice", r"eviction process", r"being evicted",
    r"lawsuit", r"suing", r"legal advice", r"legal action",
    r"attorney", r"lawyer", r"mold lawsuit",
    r"bed bug", r"cockroach", r"roach infestation",
    r"harassment", r"retaliation", r"discrimination complaint",
    r"fair housing complaint", r"restraining order",
    r"domestic violence", r"sex offender",
    r"illegal activity", r"drug bust", r"police report",
    r"code violation", r"health department", r"condemn",
]

BRIGHTPLACE_ARTICLES = {
    # Guides
    "rent|afford|budget|cost|monthly": "https://www.brightplace.ai/guides/your-true-monthly-cost",
    "how to rent|first apartment|renting process": "https://www.brightplace.ai/guides/how-to-rent-an-apartment",
    "austin|atx": "https://www.brightplace.ai/guides/austin-young-professionals",
    "brooklyn": "https://www.brightplace.ai/guides/brooklyn-neighborhood-guide",
    "charlotte": "https://www.brightplace.ai/guides/charlotte-affordable-neighborhoods",
    "chicago.*pet|chicago.*dog": "https://www.brightplace.ai/guides/chicago-pet-owners",
    "dallas|dfw|plano|frisco": "https://www.brightplace.ai/guides/dallas-families",
    "denver": "https://www.brightplace.ai/guides/denver-city-orientation",
    "san diego.*dog|sd.*dog": "https://www.brightplace.ai/guides/dog-friendly-neighborhoods-san-diego",
    "houston": "https://www.brightplace.ai/guides/houston-city-orientation",
    "kansas city|kc": "https://www.brightplace.ai/guides/kansas-city-young-professionals",
    "nashville": "https://www.brightplace.ai/guides/nashville-corporate-relocation-neighborhoods",
    "philadelphia|philly": "https://www.brightplace.ai/guides/philadelphia-city-orientation",
    "phoenix|scottsdale|chandler|gilbert": "https://www.brightplace.ai/guides/phoenix-renters-orientation",
    "salt lake|slc": "https://www.brightplace.ai/guides/salt-lake-city-renters-orientation",
    "tampa": "https://www.brightplace.ai/guides/tampa-renters-orientation",
    # Resources
    "pet friendly|pet deposit|pet rent|breed restrict": "https://www.brightplace.ai/resources/pet-friendly-apartments-greenville-sc",
    "renters insurance|roommate.*insurance": "https://www.brightplace.ai/resources/renters-insurance-with-roommates",
    "short.term lease|month to month|temporary": "https://www.brightplace.ai/resources/short-term-lease-agreement",
    "sublet|sublease|nyc.*sublet": "https://www.brightplace.ai/resources/sublet-apartments-nyc",
    "tour.*question|what to ask|apartment tour": "https://www.brightplace.ai/resources/questions-to-ask-when-touring-an-apartment",
    "dog park": "https://www.brightplace.ai/resources/apartments-with-dog-parks",
    "attached garage|garage apartment": "https://www.brightplace.ai/resources/apartments-with-attached-garages",
    "nyc.*1 bedroom|nyc.*one bedroom|1br.*nyc": "https://www.brightplace.ai/resources/one-bedroom-apartment-nyc",
    "mission beach|pacific beach": "https://www.brightplace.ai/resources/renting-mission-beach-san-diego",
    "no deposit|deposit alternative": "https://www.brightplace.ai/resources/homes-for-rent-no-deposit",
}

# Seen posts tracker file
SEEN_FILE = Path(__file__).parent / "reddit_seen_posts.json"

# --- HELPERS ---

def load_seen():
    """Load previously seen post IDs to avoid duplicates."""
    if SEEN_FILE.exists():
        with open(SEEN_FILE) as f:
            data = json.load(f)
        # Clean entries older than 3 days
        cutoff = (datetime.now() - timedelta(days=3)).isoformat()
        return {k: v for k, v in data.items() if v > cutoff}
    return {}


def save_seen(seen):
    """Save seen post IDs."""
    with open(SEEN_FILE, "w") as f:
        json.dump(seen, f, indent=2)


def post_id(post):
    """Generate a unique ID for a Reddit post."""
    return hashlib.md5((post.get("link", "") + post.get("title", "")).encode()).hexdigest()


def matches_keywords(text, keywords):
    """Check if text matches any keyword pattern."""
    text_lower = text.lower()
    for kw in keywords:
        if re.search(kw, text_lower):
            return True
    return False


def find_best_article(text):
    """Find the best matching brightplace article for the post content."""
    text_lower = text.lower()
    for pattern, url in BRIGHTPLACE_ARTICLES.items():
        if re.search(pattern, text_lower):
            return url
    return None


def fetch_subreddit(subreddit):
    """Fetch recent posts from a subreddit via RSS."""
    url = f"https://www.reddit.com/r/{subreddit}/new.rss"
    headers = {"User-Agent": "brightplace-monitor/1.0"}
    try:
        feed = feedparser.parse(url, request_headers=headers)
        posts = []
        for entry in feed.entries[:10]:  # Last 10 posts
            posts.append({
                "title": entry.get("title", ""),
                "content": entry.get("summary", ""),
                "link": entry.get("link", ""),
                "author": entry.get("author", ""),
                "published": entry.get("published", ""),
                "subreddit": subreddit,
            })
        return posts
    except Exception as e:
        print(f"  Error fetching r/{subreddit}: {e}")
        return []


def draft_answer(post):
    """Use Claude to draft a Reddit answer."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return {"relevance": "SKIP", "link_opportunity": "NONE", "link": "NONE", "answer": "No API key set"}

    prompt = f"""You are a renter education expert. You sound like a real Reddit user who knows the apartment market well. You are NOT a brand.

A Reddit user posted in r/{post['subreddit']}:

Title: {post['title']}
Body: {post['content'][:1000]}

Do these things:

1. Rate RELEVANCE: HIGH (directly about renting/apartments), MEDIUM (housing-related), LOW (tangential), SKIP (not relevant)

2. Rate LINK_OPPORTUNITY: HIGH (a brightplace article directly answers this), MEDIUM (related), LOW (weak match), NONE

3. Draft a 100-200 word answer:
   - First sentence answers the question directly
   - Include at least one specific number or dollar figure
   - Sound like a real person, NOT a company
   - Do NOT say "brightplace" in the answer
   - Be honest about tradeoffs
   - If linking, put it at the END: "There's a solid breakdown here: [URL]"
   - Do NOT link if LINK_OPPORTUNITY is LOW or NONE

Respond EXACTLY like this:

RELEVANCE: [value]
LINK_OPPORTUNITY: [value]
SUGGESTED_LINK: [URL or NONE]

DRAFTED_ANSWER:
[answer text]"""

    try:
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
        text = response.json()["content"][0]["text"]

        # Parse the response
        result = {"raw": text}
        for line in text.split("\n"):
            if line.startswith("RELEVANCE:"):
                result["relevance"] = line.split(":", 1)[1].strip()
            elif line.startswith("LINK_OPPORTUNITY:"):
                result["link_opportunity"] = line.split(":", 1)[1].strip()
            elif line.startswith("SUGGESTED_LINK:"):
                result["link"] = line.split(":", 1)[1].strip()

        # Extract drafted answer
        if "DRAFTED_ANSWER:" in text:
            result["answer"] = text.split("DRAFTED_ANSWER:", 1)[1].strip()
        else:
            result["answer"] = text

        return result

    except Exception as e:
        print(f"  Claude API error: {e}")
        return {"relevance": "SKIP", "link_opportunity": "NONE", "link": "NONE", "answer": f"Error: {e}"}


def send_to_slack(post, draft):
    """Send the opportunity to Slack via webhook."""
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook_url:
        return False

    message = {
        "text": f"🔔 *Reddit Opportunity*\n\n"
                f"*Subreddit:* r/{post['subreddit']}\n"
                f"*Post:* {post['title']}\n"
                f"*Link:* {post['link']}\n"
                f"*Relevance:* {draft.get('relevance', 'unknown')}\n"
                f"*Link Opportunity:* {draft.get('link_opportunity', 'unknown')}\n"
                f"*Suggested Link:* {draft.get('link', 'NONE')}\n\n"
                f"---\n\n"
                f"*Drafted Answer:*\n{draft.get('answer', 'No draft')}\n\n"
                f"---\n"
                f"_Copy-paste into Reddit manually if the answer is good._"
    }

    try:
        resp = requests.post(webhook_url, json=message, timeout=10)
        return resp.status_code == 200
    except Exception as e:
        print(f"  Slack error: {e}")
        return False


# --- MAIN ---

def run(tiers=None, dry_run=False, verbose=False):
    """Main monitoring loop."""
    if tiers is None:
        tiers = ["high", "city", "topical"]

    seen = load_seen()
    opportunities_found = 0
    posts_checked = 0

    print(f"\n{'='*60}")
    print(f"brightplace Reddit Monitor — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Tiers: {', '.join(tiers)}")
    print(f"{'='*60}\n")

    for tier in tiers:
        subs = SUBREDDITS.get(tier, [])
        print(f"\n--- Tier: {tier} ({len(subs)} subreddits) ---")

        for sub in subs:
            posts = fetch_subreddit(sub)
            if not posts:
                continue

            for post in posts:
                pid = post_id(post)
                posts_checked += 1

                # Skip already-seen posts
                if pid in seen:
                    continue

                text = f"{post['title']} {post['content']}"

                # Keyword filter
                if not matches_keywords(text, POSITIVE_KEYWORDS):
                    seen[pid] = datetime.now().isoformat()
                    continue

                # Negative filter
                if matches_keywords(text, NEGATIVE_KEYWORDS):
                    seen[pid] = datetime.now().isoformat()
                    continue

                # This post passed filters
                print(f"\n  ✅ r/{sub}: {post['title'][:80]}")

                # Find matching article
                suggested_article = find_best_article(text)
                if suggested_article:
                    print(f"     Article match: {suggested_article}")

                # Draft answer with Claude
                print(f"     Drafting answer...")
                draft = draft_answer(post)

                relevance = draft.get("relevance", "SKIP")
                print(f"     Relevance: {relevance}")

                if relevance == "SKIP":
                    seen[pid] = datetime.now().isoformat()
                    continue

                opportunities_found += 1

                if dry_run:
                    print(f"\n     --- DRAFT ---")
                    print(f"     {draft.get('answer', 'No draft')[:300]}")
                    print(f"     --- END DRAFT ---\n")
                else:
                    # Send to Slack
                    sent = send_to_slack(post, draft)
                    if sent:
                        print(f"     → Sent to Slack ✓")
                    else:
                        print(f"     → Slack send failed (check SLACK_WEBHOOK_URL)")

                seen[pid] = datetime.now().isoformat()

            # Rate limit: don't hammer Reddit
            time.sleep(2)

    save_seen(seen)

    print(f"\n{'='*60}")
    print(f"Done. Checked {posts_checked} posts. Found {opportunities_found} opportunities.")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="brightplace Reddit Monitor")
    parser.add_argument("--tier", choices=["high", "city", "topical", "all"], default="all",
                        help="Which tier of subreddits to check")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print results without sending to Slack")
    parser.add_argument("--verbose", action="store_true",
                        help="Print extra debug info")
    args = parser.parse_args()

    tiers = ["high", "city", "topical"] if args.tier == "all" else [args.tier]
    run(tiers=tiers, dry_run=args.dry_run, verbose=args.verbose)
