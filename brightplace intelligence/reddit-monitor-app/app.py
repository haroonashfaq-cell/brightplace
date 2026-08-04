"""brightplace Reddit Monitor — FastAPI Web App."""
import asyncio
import threading
from datetime import datetime
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from database import (
    init_db, seed_data, get_subreddits, get_all_subreddits, add_subreddit,
    toggle_subreddit, delete_subreddit, get_articles, add_article, update_article,
    delete_article, get_opportunities, get_opportunity, add_opportunity,
    update_opportunity_status, update_opportunity_draft, create_run, update_run,
    get_runs, get_setting, set_setting, get_trends,
    get_warmup_accounts, add_warmup_account, update_warmup_account,
    delete_warmup_account, add_warmup_check, get_warmup_checks
)
from scout import run_scout, post_hash, filter_post
from drafter import draft_answer, find_best_article

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))

app = FastAPI(title="brightplace Reddit Monitor")
templates = Jinja2Templates(directory=_os.path.join(_HERE, "templates"))

# Initialize database on startup
@app.on_event("startup")
async def startup():
    init_db()
    seed_data()


# --- Dashboard ---

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, status: str = None):
    opps = get_opportunities(status=status, limit=50)
    runs = get_runs(limit=5)
    stats = {
        "total": len(get_opportunities(limit=1000)),
        "pending": len(get_opportunities(status="pending", limit=1000)),
        "posted": len(get_opportunities(status="posted", limit=1000)),
        "dismissed": len(get_opportunities(status="dismissed", limit=1000)),
    }
    return templates.TemplateResponse(request, "dashboard.html", {
        "opportunities": opps,
        "runs": runs,
        "stats": stats,
        "filter_status": status,
        "page": "dashboard",
    })


# --- Run Scout ---

@app.post("/scout/run")
async def run_scout_endpoint(request: Request):
    """Run the Reddit scout in a background thread."""
    form = await request.form()
    test_mode = form.get("test_mode") == "1"

    def _run():
        subreddits = get_subreddits()
        tier_label = "test" if test_mode else "all"
        run_id = create_run(tier_label)

        try:
            posts_checked, matched = run_scout(subreddits, test_mode=test_mode)
            opportunities = 0

            seen_urls = set(o["post_url"] for o in get_opportunities(limit=500))

            for post in matched:
                if post["link"] in seen_urls:
                    continue

                result = draft_answer(post)

                if result["relevance"] == "SKIP":
                    continue

                add_opportunity(
                    run_id=run_id,
                    subreddit=post["subreddit"],
                    post_title=post["title"],
                    post_body=post.get("content", "")[:500],
                    post_url=post["link"],
                    post_author=post.get("author", ""),
                    relevance=result["relevance"],
                    link_opportunity=result["link_opportunity"],
                    suggested_link=result.get("suggested_link", ""),
                    drafted_answer=result["answer"],
                    is_promotional=1 if result.get("is_promotional") else 0,
                )
                opportunities += 1

            update_run(run_id, posts_checked, len(matched), opportunities, "completed")
        except Exception as e:
            update_run(run_id, 0, 0, 0, f"error: {str(e)}")

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()

    return RedirectResponse(url="/?running=true", status_code=303)


# --- Opportunity Actions ---

@app.post("/opportunity/{opp_id}/status")
async def update_status(opp_id: int, status: str = Form(...)):
    update_opportunity_status(opp_id, status)
    return RedirectResponse(url="/", status_code=303)


@app.post("/opportunity/{opp_id}/regenerate")
async def regenerate_draft(opp_id: int):
    opp = get_opportunity(opp_id)
    if not opp:
        raise HTTPException(status_code=404)

    post = {
        "title": opp["post_title"],
        "content": opp["post_body"],
        "subreddit": opp["subreddit"],
    }
    result = draft_answer(post, force_link=bool(opp["is_promotional"]))
    update_opportunity_draft(opp_id, result["answer"])

    return RedirectResponse(url="/", status_code=303)


# --- Knowledge Base ---

@app.get("/knowledge", response_class=HTMLResponse)
async def knowledge_page(request: Request):
    articles = get_articles()
    return templates.TemplateResponse(request, "knowledge.html", {
        "articles": articles,
        "page": "knowledge",
    })


@app.post("/knowledge/add")
async def add_article_endpoint(title: str = Form(...), url: str = Form(...), keywords: str = Form("")):
    add_article(title, url, keywords)
    return RedirectResponse(url="/knowledge", status_code=303)


@app.post("/knowledge/{art_id}/delete")
async def delete_article_endpoint(art_id: int):
    delete_article(art_id)
    return RedirectResponse(url="/knowledge", status_code=303)


# --- Settings ---

@app.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    subreddits = get_all_subreddits()
    tone = get_setting("tone_profile", "")
    ratio = get_setting("promotional_ratio", "0.20")
    return templates.TemplateResponse(request, "settings.html", {
        "subreddits": subreddits,
        "tone_profile": tone,
        "promotional_ratio": ratio,
        "page": "settings",
    })


@app.post("/settings/tone")
async def update_tone(tone_profile: str = Form(...)):
    set_setting("tone_profile", tone_profile)
    return RedirectResponse(url="/settings", status_code=303)


@app.post("/settings/ratio")
async def update_ratio(promotional_ratio: str = Form(...)):
    set_setting("promotional_ratio", promotional_ratio)
    return RedirectResponse(url="/settings", status_code=303)


@app.post("/settings/subreddit/add")
async def add_sub(name: str = Form(...), tier: str = Form("city")):
    add_subreddit(name, tier)
    return RedirectResponse(url="/settings", status_code=303)


@app.post("/settings/subreddit/{sub_id}/toggle")
async def toggle_sub(sub_id: int, enabled: int = Form(...)):
    toggle_subreddit(sub_id, enabled)
    return RedirectResponse(url="/settings", status_code=303)


@app.post("/settings/subreddit/{sub_id}/delete")
async def delete_sub(sub_id: int):
    delete_subreddit(sub_id)
    return RedirectResponse(url="/settings", status_code=303)


# --- History ---

@app.get("/history", response_class=HTMLResponse)
async def history_page(request: Request):
    runs = get_runs(limit=50)
    return templates.TemplateResponse(request, "history.html", {
        "runs": runs,
        "page": "history",
    })


# --- Trends ---

@app.get("/trends", response_class=HTMLResponse)
async def trends_page(request: Request):
    trend_data = get_trends(limit=30)
    return templates.TemplateResponse(request, "trends.html", {
        "trends": trend_data,
        "page": "trends",
    })


# --- Account Warmup ---

@app.get("/warmup", response_class=HTMLResponse)
async def warmup_page(request: Request):
    accounts = get_warmup_accounts()
    # Attach subreddit readiness to each account
    from account_checker import get_subreddit_readiness, TIER_LABELS
    for acc in accounts:
        acc["sub_readiness"] = get_subreddit_readiness(
            acc["readiness_score"], acc["account_age_days"],
            acc["karma_post"], acc["karma_comment"]
        )
        acc["tier_label"] = TIER_LABELS.get(acc["status"], "Unknown")
        acc["checks"] = get_warmup_checks(acc["id"], limit=5)
    return templates.TemplateResponse(request, "warmup.html", {
        "accounts": accounts,
        "page": "warmup",
    })


@app.post("/warmup/add")
async def warmup_add(username: str = Form(...)):
    add_warmup_account(username)
    return RedirectResponse(url="/warmup", status_code=303)


@app.get("/debug-account/{username}")
async def warmup_debug(username: str):
    """Debug: run full check and return JSON result."""
    from account_checker import run_full_check
    return run_full_check(username)


@app.post("/warmup/{account_id}/check")
async def warmup_check(account_id: int):
    from account_checker import run_full_check

    accounts = get_warmup_accounts()
    account = next((a for a in accounts if a["id"] == account_id), None)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    result = run_full_check(account["username"])
    update_warmup_account(
        account_id,
        karma_post=result.get("karma_post", 0),
        karma_comment=result.get("karma_comment", 0),
        account_age_days=result.get("account_age_days", 0),
        is_verified=result.get("is_verified", 0),
        is_shadowbanned=result.get("is_shadowbanned", 0),
        readiness_score=result.get("readiness_score", 0),
        status=result.get("status", "red"),
        last_checked=datetime.now().isoformat(),
    )
    add_warmup_check(account_id, result)

    return RedirectResponse(url="/warmup", status_code=303)


@app.post("/warmup/{account_id}/delete")
async def warmup_delete(account_id: int):
    delete_warmup_account(account_id)
    return RedirectResponse(url="/warmup", status_code=303)


@app.post("/warmup/check-all")
async def warmup_check_all():
    from account_checker import run_full_check
    import time as _time

    accounts = get_warmup_accounts()
    for account in accounts:
        try:
            result = run_full_check(account["username"])
            update_warmup_account(
                account["id"],
                karma_post=result.get("karma_post", 0),
                karma_comment=result.get("karma_comment", 0),
                account_age_days=result.get("account_age_days", 0),
                is_verified=result.get("is_verified", 0),
                is_shadowbanned=result.get("is_shadowbanned", 0),
                readiness_score=result.get("readiness_score", 0),
                status=result.get("status", "red"),
                last_checked=datetime.now().isoformat(),
            )
            add_warmup_check(account["id"], result)
            _time.sleep(2)  # Rate limit between accounts
        except Exception as e:
            print(f"Error checking {account['username']}: {e}")

    return RedirectResponse(url="/warmup", status_code=303)


@app.post("/webhook/posts")
async def webhook_receive_posts(request: Request):
    """Receive Reddit posts from n8n webhook and process them."""
    import json
    body = await request.json()

    # Accept either a single post or a list of posts
    posts = body if isinstance(body, list) else [body]

    run_id = create_run("webhook")
    posts_checked = 0
    matched_count = 0
    opportunities = 0
    seen_urls = set(o["post_url"] for o in get_opportunities(limit=500))

    for post_data in posts:
        # Normalize field names (n8n may send different keys)
        post = {
            "title": post_data.get("title", ""),
            "content": post_data.get("content", post_data.get("selftext", post_data.get("summary", ""))),
            "link": post_data.get("link", post_data.get("url", post_data.get("permalink", ""))),
            "author": post_data.get("author", "").replace("/u/", ""),
            "subreddit": post_data.get("subreddit", post_data.get("category", "unknown")),
            "score": post_data.get("score", 0),
            "num_comments": post_data.get("num_comments", 0),
        }

        posts_checked += 1

        if not filter_post(post):
            continue

        matched_count += 1
        post["tier"] = "webhook"

        if post["link"] in seen_urls:
            continue

        result = draft_answer(post)
        if result["relevance"] == "SKIP":
            continue

        add_opportunity(
            run_id=run_id,
            subreddit=post["subreddit"],
            post_title=post["title"],
            post_body=post.get("content", "")[:500],
            post_url=post["link"],
            post_author=post.get("author", ""),
            relevance=result["relevance"],
            link_opportunity=result["link_opportunity"],
            suggested_link=result.get("suggested_link", ""),
            drafted_answer=result["answer"],
            is_promotional=1 if result.get("is_promotional") else 0,
        )
        opportunities += 1

    update_run(run_id, posts_checked, matched_count, opportunities, "completed")

    return {
        "status": "ok",
        "posts_checked": posts_checked,
        "matched": matched_count,
        "opportunities": opportunities,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
