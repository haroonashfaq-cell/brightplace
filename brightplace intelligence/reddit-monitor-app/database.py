"""SQLite database models and queries."""
import sqlite3
import json
from datetime import datetime
from config import DB_PATH


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS subreddits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            tier TEXT DEFAULT 'city',
            enabled INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL,
            keywords TEXT DEFAULT '',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS opportunities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER,
            subreddit TEXT NOT NULL,
            post_title TEXT NOT NULL,
            post_body TEXT DEFAULT '',
            post_url TEXT UNIQUE NOT NULL,
            post_author TEXT DEFAULT '',
            relevance TEXT DEFAULT 'MEDIUM',
            link_opportunity TEXT DEFAULT 'NONE',
            suggested_link TEXT DEFAULT '',
            drafted_answer TEXT DEFAULT '',
            is_promotional INTEGER DEFAULT 0,
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (run_id) REFERENCES scout_runs(id)
        );

        CREATE TABLE IF NOT EXISTS scout_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tiers TEXT DEFAULT 'all',
            posts_checked INTEGER DEFAULT 0,
            posts_matched INTEGER DEFAULT 0,
            opportunities_found INTEGER DEFAULT 0,
            status TEXT DEFAULT 'running',
            started_at TEXT DEFAULT CURRENT_TIMESTAMP,
            finished_at TEXT
        );

        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS trends (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            term TEXT NOT NULL,
            count INTEGER DEFAULT 1,
            subreddit TEXT DEFAULT '',
            period TEXT DEFAULT '',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS warmup_accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            karma_post INTEGER DEFAULT 0,
            karma_comment INTEGER DEFAULT 0,
            account_age_days INTEGER DEFAULT 0,
            is_verified INTEGER DEFAULT 0,
            is_shadowbanned INTEGER DEFAULT 0,
            readiness_score INTEGER DEFAULT 0,
            status TEXT DEFAULT 'red',
            last_checked TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS warmup_checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            karma_post INTEGER DEFAULT 0,
            karma_comment INTEGER DEFAULT 0,
            account_age_days INTEGER DEFAULT 0,
            readiness_score INTEGER DEFAULT 0,
            checked_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_id) REFERENCES warmup_accounts(id)
        );
    """)
    conn.commit()
    conn.close()


# --- Subreddits ---

def get_subreddits(tier=None):
    conn = get_db()
    if tier:
        rows = conn.execute("SELECT * FROM subreddits WHERE tier = ? AND enabled = 1 ORDER BY name", (tier,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM subreddits WHERE enabled = 1 ORDER BY tier, name").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_subreddits():
    conn = get_db()
    rows = conn.execute("SELECT * FROM subreddits ORDER BY tier, name").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_subreddit(name, tier="city"):
    conn = get_db()
    try:
        conn.execute("INSERT INTO subreddits (name, tier) VALUES (?, ?)", (name, tier))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()


def toggle_subreddit(sub_id, enabled):
    conn = get_db()
    conn.execute("UPDATE subreddits SET enabled = ? WHERE id = ?", (enabled, sub_id))
    conn.commit()
    conn.close()


def delete_subreddit(sub_id):
    conn = get_db()
    conn.execute("DELETE FROM subreddits WHERE id = ?", (sub_id,))
    conn.commit()
    conn.close()


# --- Articles ---

def get_articles():
    conn = get_db()
    rows = conn.execute("SELECT * FROM articles ORDER BY title").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_article(title, url, keywords=""):
    conn = get_db()
    try:
        conn.execute("INSERT INTO articles (title, url, keywords) VALUES (?, ?, ?)", (title, url, keywords))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()


def update_article(art_id, title, url, keywords):
    conn = get_db()
    conn.execute("UPDATE articles SET title=?, url=?, keywords=? WHERE id=?", (title, url, keywords, art_id))
    conn.commit()
    conn.close()


def delete_article(art_id):
    conn = get_db()
    conn.execute("DELETE FROM articles WHERE id = ?", (art_id,))
    conn.commit()
    conn.close()


# --- Opportunities ---

def get_opportunities(status=None, limit=50):
    conn = get_db()
    if status:
        rows = conn.execute(
            "SELECT * FROM opportunities WHERE status = ? ORDER BY created_at DESC LIMIT ?",
            (status, limit)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM opportunities ORDER BY created_at DESC LIMIT ?",
            (limit,)
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_opportunity(opp_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM opportunities WHERE id = ?", (opp_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def add_opportunity(run_id, subreddit, post_title, post_body, post_url, post_author,
                    relevance, link_opportunity, suggested_link, drafted_answer, is_promotional):
    conn = get_db()
    try:
        conn.execute("""
            INSERT INTO opportunities (run_id, subreddit, post_title, post_body, post_url, post_author,
                                       relevance, link_opportunity, suggested_link, drafted_answer, is_promotional)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (run_id, subreddit, post_title, post_body, post_url, post_author,
              relevance, link_opportunity, suggested_link, drafted_answer, is_promotional))
        conn.commit()
        return conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()


def update_opportunity_status(opp_id, status):
    conn = get_db()
    conn.execute("UPDATE opportunities SET status = ? WHERE id = ?", (status, opp_id))
    conn.commit()
    conn.close()


def update_opportunity_draft(opp_id, drafted_answer):
    conn = get_db()
    conn.execute("UPDATE opportunities SET drafted_answer = ? WHERE id = ?", (drafted_answer, opp_id))
    conn.commit()
    conn.close()


# --- Scout Runs ---

def create_run(tiers="all"):
    conn = get_db()
    conn.execute("INSERT INTO scout_runs (tiers) VALUES (?)", (tiers,))
    conn.commit()
    run_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return run_id


def update_run(run_id, posts_checked, posts_matched, opportunities_found, status="completed"):
    conn = get_db()
    conn.execute("""
        UPDATE scout_runs SET posts_checked=?, posts_matched=?, opportunities_found=?,
        status=?, finished_at=? WHERE id=?
    """, (posts_checked, posts_matched, opportunities_found, status, datetime.now().isoformat(), run_id))
    conn.commit()
    conn.close()


def get_runs(limit=20):
    conn = get_db()
    rows = conn.execute("SELECT * FROM scout_runs ORDER BY started_at DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# --- Settings ---

def get_setting(key, default=""):
    conn = get_db()
    row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
    conn.close()
    return row["value"] if row else default


def set_setting(key, value):
    conn = get_db()
    conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, str(value)))
    conn.commit()
    conn.close()


# --- Trends ---

def add_trend(term, count, subreddit, period):
    conn = get_db()
    conn.execute("INSERT INTO trends (term, count, subreddit, period) VALUES (?, ?, ?, ?)",
                 (term, count, subreddit, period))
    conn.commit()
    conn.close()


def get_trends(period=None, limit=30):
    conn = get_db()
    if period:
        rows = conn.execute(
            "SELECT term, SUM(count) as total, GROUP_CONCAT(DISTINCT subreddit) as subs FROM trends WHERE period=? GROUP BY term ORDER BY total DESC LIMIT ?",
            (period, limit)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT term, SUM(count) as total, GROUP_CONCAT(DISTINCT subreddit) as subs FROM trends GROUP BY term ORDER BY total DESC LIMIT ?",
            (limit,)
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# --- Warmup Accounts ---

def get_warmup_accounts():
    conn = get_db()
    rows = conn.execute("SELECT * FROM warmup_accounts ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_warmup_account(username):
    conn = get_db()
    try:
        conn.execute("INSERT INTO warmup_accounts (username) VALUES (?)", (username.strip().lower(),))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def update_warmup_account(account_id, **data):
    conn = get_db()
    fields = []
    values = []
    for key, val in data.items():
        fields.append(f"{key} = ?")
        values.append(val)
    values.append(account_id)
    conn.execute(f"UPDATE warmup_accounts SET {', '.join(fields)} WHERE id = ?", values)
    conn.commit()
    conn.close()


def delete_warmup_account(account_id):
    conn = get_db()
    conn.execute("DELETE FROM warmup_checks WHERE account_id = ?", (account_id,))
    conn.execute("DELETE FROM warmup_accounts WHERE id = ?", (account_id,))
    conn.commit()
    conn.close()


def add_warmup_check(account_id, data):
    conn = get_db()
    conn.execute("""
        INSERT INTO warmup_checks (account_id, karma_post, karma_comment, account_age_days, readiness_score)
        VALUES (?, ?, ?, ?, ?)
    """, (account_id, data.get("karma_post", 0), data.get("karma_comment", 0),
          data.get("account_age_days", 0), data.get("readiness_score", 0)))
    conn.commit()
    conn.close()


def get_warmup_checks(account_id, limit=20):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM warmup_checks WHERE account_id = ? ORDER BY checked_at DESC LIMIT ?",
        (account_id, limit)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# --- Seed ---

def seed_data():
    """Seed default subreddits and articles if tables are empty."""
    from config import DEFAULT_SUBREDDITS, DEFAULT_ARTICLES, DEFAULT_TONE

    conn = get_db()

    # Seed subreddits
    count = conn.execute("SELECT COUNT(*) FROM subreddits").fetchone()[0]
    if count == 0:
        for tier, subs in DEFAULT_SUBREDDITS.items():
            for sub in subs:
                try:
                    conn.execute("INSERT INTO subreddits (name, tier) VALUES (?, ?)", (sub, tier))
                except sqlite3.IntegrityError:
                    pass
        conn.commit()

    # Seed articles
    count = conn.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
    if count == 0:
        for art in DEFAULT_ARTICLES:
            try:
                conn.execute("INSERT INTO articles (title, url, keywords) VALUES (?, ?, ?)",
                             (art["title"], art["url"], art["keywords"]))
            except sqlite3.IntegrityError:
                pass
        conn.commit()

    # Seed settings
    if not get_setting("tone_profile"):
        set_setting("tone_profile", DEFAULT_TONE)
    if not get_setting("promotional_ratio"):
        set_setting("promotional_ratio", "0.20")

    conn.close()
