"""Modal deployment for brightplace Reddit Monitor."""
import modal
import os

app = modal.App("brightplace-reddit-monitor")

image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "fastapi",
        "uvicorn",
        "jinja2",
        "python-multipart",
        "feedparser",
        "anthropic",
        "requests",
        "python-dotenv",
    )
    .add_local_dir(".", remote_path="/app")
)

volume = modal.Volume.from_name("reddit-monitor-db", create_if_missing=True)


def _setup():
    """Common setup for both web and scheduled functions."""
    import sys
    os.chdir("/app")
    sys.path.insert(0, "/app")
    os.environ["DB_PATH"] = "/data/reddit_monitor.db"
    import config
    config.DB_PATH = "/data/reddit_monitor.db"
    from database import init_db, seed_data
    init_db()
    seed_data()


@app.function(
    image=image,
    volumes={"/data": volume},
    secrets=[modal.Secret.from_name("reddit-monitor-secrets")],
    allow_concurrent_inputs=10,
    timeout=600,
)
@modal.asgi_app()
def web():
    _setup()
    from app import app as fastapi_app
    return fastapi_app


@app.function(
    image=image,
    volumes={"/data": volume},
    secrets=[modal.Secret.from_name("reddit-monitor-secrets")],
    timeout=600,
    schedule=modal.Cron("0 * * * *"),  # Every hour
)
def scheduled_scout():
    """Auto-run scout 3 times a day."""
    _setup()

    from database import (
        get_subreddits, get_opportunities, create_run, update_run, add_opportunity
    )
    from scout import run_scout
    from drafter import draft_answer

    subreddits = get_subreddits()
    run_id = create_run("scheduled")

    try:
        posts_checked, matched = run_scout(subreddits)
        opportunities = 0
        seen_urls = set(o["post_url"] for o in get_opportunities(limit=500))

        for post in matched:
            if post["link"] in seen_urls:
                continue
            result = draft_answer(post)
            if result["relevance"] == "SKIP":
                continue
            add_opportunity(
                run_id=run_id, subreddit=post["subreddit"],
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
        print(f"Scout complete: {posts_checked} checked, {len(matched)} matched, {opportunities} new")

    except Exception as e:
        update_run(run_id, 0, 0, 0, f"error: {str(e)}")
        print(f"Scout error: {e}")

    volume.commit()


