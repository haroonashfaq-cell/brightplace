"""Reddit account health checker — uses RSS + old.reddit to check
   account status, karma, activity, and ban/suspension state.

   Makes exactly 2 HTTP requests per check:
   1. RSS feed (primary — works from datacenter IPs)
   2. old.reddit profile (for karma — may be blocked from datacenters)
"""
import re
import time
import requests
from datetime import datetime, timezone


def _session():
    """Create a requests session with browser-like headers."""
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    })
    return s


def run_full_check(username):
    """Single function that runs the complete health check.
    Makes exactly 2 requests: RSS then old.reddit.
    Returns dict ready for DB update."""
    result = {
        "username": username,
        "karma_post": 0,
        "karma_comment": 0,
        "account_age_days": 0,
        "is_verified": 0,
        "recent_activity": 0,
        "is_suspended": False,
        "is_shadowbanned": 0,
        "readiness_score": 0,
        "status": "red",
        "error": None,
    }

    s = _session()

    # ═══ Request 1: RSS feed ═══
    rss_suspended = False

    rss = s.get(f"https://www.reddit.com/user/{username}/.rss", timeout=15)
    result["_rss_status"] = rss.status_code
    result["_rss_len"] = len(rss.text)

    if rss.status_code == 200 and "<?xml" in rss.text[:200]:
        entries = re.findall(r"<entry>", rss.text)
        result["recent_activity"] = len(entries)

        dates = re.findall(r"<updated>([^<]+)</updated>", rss.text)
        if dates:
            result["account_age_days"] = _parse_datetime_age(dates[-1])

        if entries:
            result["karma_comment"] = max(1, len(entries))

    elif rss.status_code == 404:
        rss_suspended = True

    elif rss.status_code == 403:
        if "<?xml" in rss.text[:200] and "<entry>" not in rss.text:
            rss_suspended = True

    elif rss.status_code == 429:
        result["error"] = "Rate limited - try again in a minute"

    if rss_suspended:
        result["is_suspended"] = True
        result["is_shadowbanned"] = 1
        return result

    # ═══ Request 2: old.reddit profile (for karma + suspension confirmation) ═══
    time.sleep(2)

    try:
        old = s.get(f"https://old.reddit.com/user/{username}", timeout=15)

        # Check for suspension markers
        title = re.findall(r"<title>([^<]+)</title>", old.text)
        title_text = title[0].lower() if title else ""

        if "suspended" in title_text or "interstitial-image-banned" in old.text:
            result["is_suspended"] = True
            result["is_shadowbanned"] = 1
            result["readiness_score"] = 0
            return result

        # If old.reddit loaded properly (200), extract karma
        if old.status_code == 200:
            # Parse karma
            karma_vals = re.findall(r'class="karma[^"]*"[^>]*>([^<]+)', old.text)
            if len(karma_vals) >= 2:
                result["karma_post"] = _parse_num(karma_vals[0])
                result["karma_comment"] = _parse_num(karma_vals[1])
            elif len(karma_vals) == 1:
                total = _parse_num(karma_vals[0])
                result["karma_post"] = total // 2
                result["karma_comment"] = total - (total // 2)

            # Explicit karma labels
            pk = re.findall(r"post karma.*?>([\d,]+)", old.text, re.DOTALL | re.IGNORECASE)
            ck = re.findall(r"comment karma.*?>([\d,]+)", old.text, re.DOTALL | re.IGNORECASE)
            if pk:
                result["karma_post"] = _parse_num(pk[0])
            if ck:
                result["karma_comment"] = _parse_num(ck[0])

            # Account creation date (more precise than RSS)
            dts = re.findall(r'datetime="([^"]+)"', old.text)
            if dts:
                age = _parse_datetime_age(dts[0])
                if age > 0:
                    result["account_age_days"] = age

            # Activity from page
            things = len(re.findall(r'class="thing"', old.text))
            if things > result["recent_activity"]:
                result["recent_activity"] = things

            # Verified email
            if "has-verified-email" in old.text.lower():
                result["is_verified"] = 1

        # If old.reddit was blocked (403) but RSS worked, that's fine
        # We just won't have exact karma — RSS estimates are used instead

    except Exception:
        pass  # old.reddit failure is non-fatal, RSS data is still valid

    # ═══ Calculate score ═══
    result["readiness_score"] = calculate_readiness_score(result)
    result["status"] = get_tier(result["readiness_score"])

    return result


def _parse_num(s):
    """Parse '1,234' or '1.2k' into int."""
    s = s.strip().replace(",", "")
    if not s:
        return 0
    low = s.lower()
    if "k" in low:
        return int(float(low.replace("k", "")) * 1000)
    if "m" in low:
        return int(float(low.replace("m", "")) * 1000000)
    try:
        return int(s)
    except ValueError:
        return 0


def _parse_datetime_age(dt_str):
    """Parse ISO datetime into account age in days."""
    now = datetime.now(timezone.utc)
    for fmt in ["%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S"]:
        try:
            dt = datetime.strptime(dt_str.strip(), fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return max(0, (now - dt).days)
        except ValueError:
            continue
    return 0


def calculate_readiness_score(data):
    """Calculate warmup readiness score (0-100)."""
    score = 0

    # Account age: 25%
    age = data.get("account_age_days", 0)
    if age >= 365: age_s = 100
    elif age >= 91: age_s = 75
    elif age >= 31: age_s = 50
    elif age >= 8: age_s = 25
    else: age_s = 0
    score += age_s * 0.25

    # Total karma: 20%
    tk = data.get("karma_post", 0) + data.get("karma_comment", 0)
    if tk >= 500: tk_s = 100
    elif tk >= 201: tk_s = 75
    elif tk >= 51: tk_s = 50
    elif tk >= 11: tk_s = 25
    else: tk_s = 0
    score += tk_s * 0.20

    # Comment karma: 15%
    ck = data.get("karma_comment", 0)
    if ck >= 100: ck_s = 100
    elif ck >= 51: ck_s = 70
    elif ck >= 11: ck_s = 40
    else: ck_s = 0
    score += ck_s * 0.15

    # Activity count: 15%
    act = data.get("recent_activity", 0)
    if act >= 50: act_s = 100
    elif act >= 21: act_s = 70
    elif act >= 6: act_s = 40
    else: act_s = 0
    score += act_s * 0.15

    # Email verified: 10%
    score += (100 if data.get("is_verified", 0) else 0) * 0.10

    # Activity presence: 15%
    if act >= 3: pres = 100
    elif act >= 1: pres = 50
    else: pres = 0
    score += pres * 0.15

    return round(score)


def get_tier(score):
    if score >= 91: return "blue"
    elif score >= 76: return "green"
    elif score >= 51: return "yellow"
    elif score >= 26: return "orange"
    else: return "red"


TIER_LABELS = {
    "red": "Not Ready",
    "orange": "Early Warmup",
    "yellow": "Warming Up",
    "green": "Ready",
    "blue": "Fully Established",
}

SUBREDDIT_THRESHOLDS = {
    "personalfinance": {"min_age": 30, "min_karma": 100, "min_comment_karma": 50},
    "AskNYC": {"min_age": 7, "min_karma": 10, "min_comment_karma": 5},
    "apartments": {"min_age": 3, "min_karma": 5, "min_comment_karma": 1},
    "renting": {"min_age": 3, "min_karma": 5, "min_comment_karma": 1},
    "FirstTimeRenter": {"min_age": 3, "min_karma": 5, "min_comment_karma": 1},
    "ApartmentHunting": {"min_age": 3, "min_karma": 5, "min_comment_karma": 1},
    "Frugal": {"min_age": 7, "min_karma": 25, "min_comment_karma": 10},
    "RealEstate": {"min_age": 14, "min_karma": 50, "min_comment_karma": 20},
    "askdfw": {"min_age": 7, "min_karma": 10, "min_comment_karma": 5},
    "Denver": {"min_age": 7, "min_karma": 10, "min_comment_karma": 5},
    "Charlotte": {"min_age": 7, "min_karma": 10, "min_comment_karma": 5},
    "Austin": {"min_age": 7, "min_karma": 10, "min_comment_karma": 5},
    "phoenix": {"min_age": 7, "min_karma": 10, "min_comment_karma": 5},
    "Philadelphia": {"min_age": 7, "min_karma": 10, "min_comment_karma": 5},
    "nashville": {"min_age": 7, "min_karma": 10, "min_comment_karma": 5},
    "SanDiego": {"min_age": 7, "min_karma": 10, "min_comment_karma": 5},
    "houston": {"min_age": 7, "min_karma": 10, "min_comment_karma": 5},
    "Tampa": {"min_age": 7, "min_karma": 10, "min_comment_karma": 5},
    "Chicago": {"min_age": 7, "min_karma": 10, "min_comment_karma": 5},
    "Atlanta": {"min_age": 7, "min_karma": 10, "min_comment_karma": 5},
    "Seattle": {"min_age": 14, "min_karma": 25, "min_comment_karma": 10},
    "MinneapolisMN": {"min_age": 7, "min_karma": 10, "min_comment_karma": 5},
    "SaltLakeCity": {"min_age": 7, "min_karma": 10, "min_comment_karma": 5},
    "kansascity": {"min_age": 7, "min_karma": 10, "min_comment_karma": 5},
    "Columbus": {"min_age": 7, "min_karma": 10, "min_comment_karma": 5},
    "Knoxville": {"min_age": 7, "min_karma": 10, "min_comment_karma": 5},
    "raleigh": {"min_age": 7, "min_karma": 10, "min_comment_karma": 5},
    "dogs": {"min_age": 3, "min_karma": 5, "min_comment_karma": 1},
    "RemoteWork": {"min_age": 3, "min_karma": 5, "min_comment_karma": 1},
}


def get_subreddit_readiness(score, account_age, karma_post, karma_comment):
    """Return list of subs with safe/risky/blocked status."""
    total_karma = karma_post + karma_comment
    results = []
    for sub, t in SUBREDDIT_THRESHOLDS.items():
        age_ok = account_age >= t["min_age"]
        karma_ok = total_karma >= t["min_karma"]
        ck_ok = karma_comment >= t["min_comment_karma"]
        if age_ok and karma_ok and ck_ok:
            status = "safe"
        elif (age_ok and karma_ok) or (age_ok and ck_ok):
            status = "risky"
        else:
            status = "blocked"
        results.append({"subreddit": sub, "status": status})
    order = {"safe": 0, "risky": 1, "blocked": 2}
    results.sort(key=lambda x: (order[x["status"]], x["subreddit"]))
    return results
