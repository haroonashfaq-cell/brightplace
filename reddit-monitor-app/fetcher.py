"""
brightplace Reddit Fetcher — runs locally, sends posts to Modal app.

Usage:
    python fetcher.py              # Run once
    python fetcher.py --loop 4h    # Run every 4 hours
    python fetcher.py --loop 30m   # Run every 30 minutes

Reddit blocks cloud IPs but allows local/residential IPs.
This script fetches RSS from your machine and sends posts to the app webhook.
"""
import re
import sys
import time
import json
import signal
import argparse
import requests
import feedparser
from html import unescape
from datetime import datetime

# --- Config ---
APP_URL = "https://haroonashfaq0121--brightplace-reddit-monitor-web.modal.run"
WEBHOOK_PATH = "/webhook/posts"
DELAY_BETWEEN_SUBS = 8  # seconds between subreddit fetches
RATE_LIMIT_WAIT = 30    # seconds to wait on 429
MAX_RETRIES = 2
RSS_USER_AGENT = "Mozilla/5.0 (compatible; n8n)"

SUBREDDITS = [
    # High-priority
    "apartments", "renting", "personalfinance",
    "FirstTimeRenter", "Frugal",
    # City
    "AskNYC", "askdfw", "Denver", "Charlotte", "Austin", "phoenix",
    "Philadelphia", "nashville", "SanDiego", "houston", "Tampa",
    "Chicago", "Atlanta", "Seattle", "MinneapolisMN", "SaltLakeCity",
    "kansascity", "Columbus", "Knoxville", "raleigh",
    # Topical
    "dogs", "RemoteWork", "RealEstate",
]


def fetch_rss(subreddit):
    """Fetch RSS feed for a subreddit with retry logic."""
    url = f"https://www.reddit.com/r/{subreddit}/new/.rss"
    headers = {"User-Agent": RSS_USER_AGENT}

    for attempt in range(MAX_RETRIES + 1):
        try:
            resp = requests.get(url, headers=headers, timeout=15)

            if resp.status_code == 429:
                wait = int(resp.headers.get("Retry-After", RATE_LIMIT_WAIT))
                print(f"  r/{subreddit}: Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue

            if resp.status_code == 403:
                print(f"  r/{subreddit}: Forbidden (403), skipping")
                return []

            if resp.status_code != 200:
                print(f"  r/{subreddit}: HTTP {resp.status_code}")
                return []

            feed = feedparser.parse(resp.content)
            posts = []

            for entry in feed.entries[:15]:
                raw_html = entry.get("summary", "")
                text = re.sub(r"<[^>]+>", " ", unescape(raw_html)).strip()
                text = re.sub(r"\s+", " ", text)
                text = re.sub(r"\s*submitted by /u/\S+.*$", "", text)

                posts.append({
                    "title": entry.get("title", ""),
                    "content": text[:500],
                    "link": entry.get("link", ""),
                    "author": entry.get("author", "").replace("/u/", ""),
                    "subreddit": subreddit,
                })

            return posts

        except requests.exceptions.Timeout:
            print(f"  r/{subreddit}: Timeout (attempt {attempt + 1})")
        except Exception as e:
            print(f"  r/{subreddit}: Error - {e}")
            return []

    return []


def run_fetch_cycle():
    """Fetch all subreddits and send to webhook."""
    start = datetime.now()
    print(f"\n{'='*60}")
    print(f"Scout run started at {start.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")

    all_posts = []
    fetched_count = 0

    for i, sub in enumerate(SUBREDDITS):
        posts = fetch_rss(sub)
        all_posts.extend(posts)
        fetched_count += 1

        status = f"  r/{sub}: {len(posts)} posts"
        print(f"  [{i+1}/{len(SUBREDDITS)}] {status}")

        if i < len(SUBREDDITS) - 1:
            time.sleep(DELAY_BETWEEN_SUBS)

    print(f"\nTotal: {len(all_posts)} posts from {fetched_count} subreddits")

    if not all_posts:
        print("No posts fetched. Skipping webhook.")
        return

    # Send to webhook in batches of 20
    batch_size = 20
    total_matched = 0
    total_opps = 0

    for i in range(0, len(all_posts), batch_size):
        batch = all_posts[i:i + batch_size]
        try:
            resp = requests.post(
                f"{APP_URL}{WEBHOOK_PATH}",
                json=batch,
                timeout=300,
            )
            if resp.status_code == 200:
                result = resp.json()
                total_matched += result.get("matched", 0)
                total_opps += result.get("opportunities", 0)
                print(f"  Batch {i//batch_size + 1}: {result.get('matched', 0)} matched, {result.get('opportunities', 0)} opportunities")
            else:
                print(f"  Batch {i//batch_size + 1}: Webhook error {resp.status_code}")
        except Exception as e:
            print(f"  Batch {i//batch_size + 1}: Send error - {e}")

    elapsed = (datetime.now() - start).total_seconds()
    print(f"\nDone in {elapsed:.0f}s — {total_matched} matched, {total_opps} new opportunities")
    print(f"Dashboard: {APP_URL}")


def parse_interval(s):
    """Parse interval string like '4h', '30m', '1h30m' to seconds."""
    total = 0
    for match in re.finditer(r"(\d+)\s*(h|m|s)", s.lower()):
        val = int(match.group(1))
        unit = match.group(2)
        if unit == "h":
            total += val * 3600
        elif unit == "m":
            total += val * 60
        elif unit == "s":
            total += val
    return total or int(s) if s.isdigit() else total


def main():
    parser = argparse.ArgumentParser(description="brightplace Reddit Fetcher")
    parser.add_argument("--loop", type=str, default=None,
                        help="Run repeatedly (e.g., --loop 4h, --loop 30m)")
    parser.add_argument("--url", type=str, default=None,
                        help="Override the app URL")
    args = parser.parse_args()

    global APP_URL
    if args.url:
        APP_URL = args.url.rstrip("/")

    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print("\nStopping fetcher...")
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    if args.loop:
        interval = parse_interval(args.loop)
        if interval < 60:
            print("Minimum interval is 1 minute.")
            sys.exit(1)

        print(f"Running every {interval//3600}h {(interval%3600)//60}m")
        print(f"App: {APP_URL}")
        print(f"Press Ctrl+C to stop.\n")

        while True:
            run_fetch_cycle()
            next_run = datetime.now().timestamp() + interval
            next_str = datetime.fromtimestamp(next_run).strftime("%H:%M:%S")
            print(f"\nNext run at {next_str}. Sleeping...")
            time.sleep(interval)
    else:
        run_fetch_cycle()


if __name__ == "__main__":
    main()
