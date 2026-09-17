"""Browser-based Reddit scraper — opens real Chrome window, scrapes posts,
   pushes them to the Modal webhook for processing."""
import re
import sys
import time
import json
import random
import requests
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from config import POSTS_PER_SUBREDDIT
from database import init_db, seed_data, get_subreddits
from scout import filter_post

MODAL_WEBHOOK_URL = "https://haroonashfaq0121--brightplace-reddit-monitor-web.modal.run/webhook/posts"
BATCH_SIZE = 20


def create_driver():
    """Create a real (non-headless) Chrome browser to bypass Reddit bot detection."""
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--window-size=1280,900")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script(
        'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    )
    return driver


def is_blocked(driver):
    """Check if Reddit returned a block/verification page."""
    try:
        src = driver.page_source.lower()
        return any(phrase in src for phrase in [
            "blocked by network security",
            "you've been blocked",
            "please wait for verification",
            "access denied",
        ])
    except Exception:
        return False


def wait_for_posts(driver, subreddit, max_wait=30):
    """Wait for posts to appear on the page, detecting blocks quickly."""
    for i in range(max_wait // 2):
        time.sleep(2)

        if i >= 1 and is_blocked(driver):
            print(f"  r/{subreddit}: Blocked by Reddit, skipping")
            return False

        try:
            count = driver.execute_script(
                "return document.querySelectorAll('shreddit-post').length"
            )
            if count and count > 0:
                print(f"  r/{subreddit}: Page loaded ({count} posts)")
                return True
        except Exception:
            pass

    print(f"  r/{subreddit}: Timed out, skipping")
    return False


def scrape_subreddit(driver, subreddit, limit=None):
    """Scrape posts from a subreddit using a real browser."""
    if limit is None:
        limit = POSTS_PER_SUBREDDIT

    url = f"https://www.reddit.com/r/{subreddit}/new/"
    print(f"  Loading r/{subreddit}...")
    driver.get(url)

    if not wait_for_posts(driver, subreddit):
        return []

    # Scroll to load more posts
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(2)

    raw = driver.execute_script("""
        var posts = document.querySelectorAll('shreddit-post');
        var data = [];
        posts.forEach(function(p) {
            var bodyEl = p.querySelector('[slot="text-body"]');
            var body = bodyEl ? bodyEl.innerText : '';
            data.push({
                title: p.getAttribute('post-title') || '',
                permalink: p.getAttribute('permalink') || '',
                author: p.getAttribute('author') || '',
                subreddit: (p.getAttribute('subreddit-prefixed-name') || '').replace('r/', ''),
                score: parseInt(p.getAttribute('score') || '0'),
                comment_count: parseInt(p.getAttribute('comment-count') || '0'),
                content: body
            });
        });
        return data;
    """) or []

    posts = []
    for p in raw[:limit]:
        permalink = p.get("permalink", "")
        link = f"https://www.reddit.com{permalink}" if permalink else ""
        posts.append({
            "title": p.get("title", ""),
            "content": p.get("content", ""),
            "link": link,
            "author": p.get("author", ""),
            "subreddit": p.get("subreddit", subreddit),
            "score": p.get("score", 0),
            "num_comments": p.get("comment_count", 0),
        })
    return posts


def push_to_modal(posts):
    """Send posts to the Modal webhook for filtering, drafting, and storage."""
    if not posts:
        return {"posts_checked": 0, "matched": 0, "opportunities": 0}

    total = {"posts_checked": 0, "matched": 0, "opportunities": 0}

    # Send in batches
    for i in range(0, len(posts), BATCH_SIZE):
        batch = posts[i:i + BATCH_SIZE]
        print(f"  Sending batch {i // BATCH_SIZE + 1} ({len(batch)} posts) to Modal...")
        try:
            resp = requests.post(MODAL_WEBHOOK_URL, json=batch, timeout=180)
            if resp.status_code == 200:
                data = resp.json()
                total["posts_checked"] += data.get("posts_checked", 0)
                total["matched"] += data.get("matched", 0)
                total["opportunities"] += data.get("opportunities", 0)
                print(f"    Checked: {data.get('posts_checked', 0)}, "
                      f"Matched: {data.get('matched', 0)}, "
                      f"Opportunities: {data.get('opportunities', 0)}")
            else:
                print(f"    Error: HTTP {resp.status_code}")
        except Exception as e:
            print(f"    Error: {e}")

    return total


def run_browser_scout(subreddit_names=None, limit_subs=None):
    """Scrape Reddit via browser and push posts to Modal for processing."""
    init_db()
    seed_data()

    subreddits = get_subreddits()
    if subreddit_names:
        subreddits = [s for s in subreddits if s["name"] in subreddit_names]
    if limit_subs:
        subreddits = subreddits[:limit_subs]

    print(f"\n{'='*60}")
    print(f"  brightplace Reddit Browser Scout")
    print(f"  Scanning {len(subreddits)} subreddits")
    print(f"  Pushing to Modal dashboard")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}\n")

    driver = create_driver()

    # Warm up session
    print("Warming up browser session...")
    driver.get("https://www.reddit.com/")
    time.sleep(5)

    if is_blocked(driver):
        print("Reddit blocked homepage. Waiting 10s and retrying...")
        time.sleep(10)
        driver.get("https://www.reddit.com/")
        time.sleep(5)

    all_posts = []
    blocked_subs = []
    scraped_subs = []

    try:
        for i, sub in enumerate(subreddits):
            print(f"\n[{i+1}/{len(subreddits)}] Scanning r/{sub['name']}...")
            posts = scrape_subreddit(driver, sub["name"])

            if len(posts) == 0:
                blocked_subs.append(sub["name"])
            else:
                scraped_subs.append(sub["name"])

            all_posts.extend(posts)

            # Random delay between subreddits (3-6s)
            if i < len(subreddits) - 1:
                delay = random.uniform(3, 6)
                time.sleep(delay)

    finally:
        driver.quit()
        print("\nBrowser closed.")

    # Summary of scraping
    print(f"\n--- Scraping Summary ---")
    print(f"  Scraped: {len(scraped_subs)} subreddits ({len(all_posts)} posts)")
    if blocked_subs:
        print(f"  Blocked: {len(blocked_subs)} subs ({', '.join(blocked_subs)})")

    # Push all posts to Modal webhook
    print(f"\n--- Pushing to Modal ---")
    result = push_to_modal(all_posts)

    print(f"\n{'='*60}")
    print(f"  SCOUT COMPLETE")
    print(f"  Posts scraped: {len(all_posts)}")
    print(f"  Posts checked: {result['posts_checked']}")
    print(f"  Keyword matches: {result['matched']}")
    print(f"  New opportunities: {result['opportunities']}")
    if blocked_subs:
        print(f"  Blocked subs: {', '.join(blocked_subs)}")
    print(f"{'='*60}\n")

    modal_url = MODAL_WEBHOOK_URL.replace("/webhook/posts", "")
    print(f"View dashboard: {modal_url}")

    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Browser-based Reddit Scout")
    parser.add_argument("--subs", nargs="*", help="Specific subreddits to scan")
    parser.add_argument("--limit", type=int, help="Max number of subreddits to scan")
    args = parser.parse_args()

    run_browser_scout(
        subreddit_names=args.subs,
        limit_subs=args.limit,
    )
