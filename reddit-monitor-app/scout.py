"""Reddit Scout — fetches and filters Reddit posts via RSS feeds."""
import re
import time
import hashlib
import requests
import feedparser
from html import unescape
from config import POSITIVE_KEYWORDS, NEGATIVE_KEYWORDS, POSTS_PER_SUBREDDIT

RSS_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
RSS_DELAY_SECONDS = 1  # 1s between requests


def fetch_subreddit(subreddit, limit=None):
    """Fetch recent posts from a subreddit via RSS feed."""
    if limit is None:
        limit = POSTS_PER_SUBREDDIT

    url = f"https://www.reddit.com/r/{subreddit}/new/.rss"
    headers = {"User-Agent": RSS_USER_AGENT}

    try:
        resp = requests.get(url, headers=headers, timeout=15)

        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", 10))
            print(f"  r/{subreddit}: Rate limited, waiting {retry_after}s...")
            time.sleep(retry_after)
            resp = requests.get(url, headers=headers, timeout=15)

        if resp.status_code != 200:
            print(f"  r/{subreddit}: HTTP {resp.status_code}")
            return []

        feed = feedparser.parse(resp.content)

        posts = []
        for entry in feed.entries[:limit]:
            # Extract text content from HTML summary
            raw_html = entry.get("summary", "")
            text_content = re.sub(r"<[^>]+>", " ", unescape(raw_html)).strip()
            text_content = re.sub(r"\s+", " ", text_content)
            # Remove the "submitted by /u/... [link] [comments]" suffix
            text_content = re.sub(r"\s*submitted by /u/\S+.*$", "", text_content)

            posts.append({
                "title": entry.get("title", ""),
                "content": text_content,
                "link": entry.get("link", ""),
                "author": entry.get("author", "").replace("/u/", ""),
                "published": entry.get("published", ""),
                "subreddit": subreddit,
                "score": 0,
                "num_comments": 0,
            })

        return posts

    except requests.exceptions.Timeout:
        print(f"  r/{subreddit}: Timeout")
        return []
    except Exception as e:
        print(f"  r/{subreddit}: Error - {e}")
        return []


def matches_positive(text):
    """Check if text matches any positive keyword."""
    text_lower = text.lower()
    for kw in POSITIVE_KEYWORDS:
        if re.search(kw, text_lower):
            return True
    return False


def matches_negative(text):
    """Check if text matches any negative keyword."""
    text_lower = text.lower()
    for kw in NEGATIVE_KEYWORDS:
        if re.search(kw, text_lower):
            return True
    return False


def filter_post(post):
    """Returns True if the post is relevant and should be drafted."""
    # Warmup posts skip keyword filtering — all posts are valid
    if post.get("tier") == "warmup":
        return True

    text = f"{post['title']} {post['content']}"

    if not matches_positive(text):
        return False

    if matches_negative(text):
        return False

    return True


def post_hash(post):
    """Generate a unique hash for deduplication."""
    return hashlib.md5((post.get("link", "") + post.get("title", "")).encode()).hexdigest()


def run_scout(subreddits, test_mode=False):
    """
    Fetch and filter posts from a list of subreddits.
    Returns (posts_checked, matched_posts).
    """
    posts_checked = 0
    matched = []

    if test_mode:
        print("  Running in TEST MODE with sample posts...")
        test_posts = get_test_posts()
        for post in test_posts:
            posts_checked += 1
            if filter_post(post):
                post["tier"] = "high"
                matched.append(post)
        print(f"  Test: {posts_checked} checked, {len(matched)} matched")
        return posts_checked, matched

    for sub in subreddits:
        tier = sub.get("tier", "unknown")
        # Warmup: 3 posts, regular: 5 posts (enough for hourly runs)
        limit = 3 if tier == "warmup" else 5
        posts = fetch_subreddit(sub["name"], limit=limit)
        print(f"  r/{sub['name']}: {len(posts)} posts fetched")

        for post in posts:
            posts_checked += 1
            post["tier"] = tier
            if filter_post(post):
                matched.append(post)

        time.sleep(RSS_DELAY_SECONDS)

    return posts_checked, matched


def get_test_posts():
    """Sample posts for pipeline testing."""
    return [
        {
            "title": "First time renter - how much should I budget for move-in costs?",
            "content": "Moving to Austin for a new job. Never rented before. Found a place for $1,400/month but confused about extra costs. Security deposit, pet deposit, application fees. Budget is about $4,000 saved.",
            "link": "https://www.reddit.com/r/ApartmentHunting/comments/test001",
            "author": "newrenter2026",
            "published": "",
            "subreddit": "ApartmentHunting",
            "score": 24,
            "num_comments": 12,
        },
        {
            "title": "Pet friendly apartments in Denver that allow large breeds?",
            "content": "I have a 70lb German Shepherd mix and every apartment has a 50lb weight limit or breed restrictions. Budget around $1,800/month for a 1-bedroom.",
            "link": "https://www.reddit.com/r/Denver/comments/test002",
            "author": "bigdogdenver",
            "published": "",
            "subreddit": "Denver",
            "score": 31,
            "num_comments": 18,
        },
        {
            "title": "Is $22/hr enough to afford rent in Phoenix?",
            "content": "Job offer in Phoenix at $22/hour. Following the 30% rule I should spend max $1,056 on rent. Can I find a studio in Tempe or Chandler?",
            "link": "https://www.reddit.com/r/phoenix/comments/test003",
            "author": "phx_mover",
            "published": "",
            "subreddit": "phoenix",
            "score": 15,
            "num_comments": 22,
        },
        {
            "title": "Questions to ask when touring an apartment?",
            "content": "First apartment tour tomorrow. What are must-ask questions? I've heard check water pressure and outlets. This is in Charlotte, NC.",
            "link": "https://www.reddit.com/r/Charlotte/comments/test004",
            "author": "clt_apartment",
            "published": "",
            "subreddit": "Charlotte",
            "score": 42,
            "num_comments": 35,
        },
    ]
