# 07 — How We Go From Local to Production

## The Question
Right now everything runs on your PC via Claude Code. How do we make this a real product that operators use in a browser?

## The Answer: Three Layers

### Layer 1: Agent Logic (Already Built)
The 6 agents (keyword, brief, writing, QA, image, publish) are system prompts. They work by:
1. Taking an input (keyword, brief, article)
2. Sending it to Claude with the agent's rules as the system prompt
3. Getting structured output back

**To productionize:** Each agent becomes a Claude API call with its markdown file as the system prompt.

```javascript
// Example: Brief Agent as an API call
const response = await anthropic.messages.create({
  model: "claude-sonnet-4-20250514",
  system: briefAgentPrompt, // contents of brief-agent.md
  messages: [{ role: "user", content: `Generate brief for keyword: ${keyword}` }],
})
```

### Layer 2: Orchestration (Backend)
A Node.js backend that:
1. Receives "approve keyword" from the dashboard
2. Calls Brief Agent (Claude API)
3. Calls Writing Agent (Claude API)
4. Calls QA Agent (Claude API)
5. Calls Publish Agent (git push or CMS API)
6. Updates status in Supabase at each step

**This is a job queue.** Each step depends on the previous. If any fails, it retries or alerts.

```
Supabase (keyword approved)
  → Backend triggers Brief Agent
    → Brief saved to Supabase
      → Backend triggers Writing Agent
        → Article saved to Supabase
          → Backend triggers QA Agent
            → QA report saved
              → Backend triggers Publish Agent
                → Published URL saved
```

### Layer 3: Dashboard (Frontend)
A Next.js app where operators:
1. Log in (Supabase Auth)
2. See keyword suggestions (from Semrush API + Keyword Agent)
3. Approve/reject keywords
4. Watch articles move through the pipeline
5. See published articles and their traffic

**The dashboard reads from Supabase and triggers backend jobs.**

## Where Does Each Piece Live?

| Component | Location | Technology |
|---|---|---|
| Agent prompts | `brightplace direct/Agents/*.md` | Markdown → Claude API system prompts |
| Backend API | `seo-product/backend/` or new repo | Node.js + Supabase + Claude API |
| Dashboard | `seo-product/frontend/` or new repo | Next.js on Vercel |
| Operator data | Supabase | PostgreSQL |
| Operator sites | `operator-pages/` | Next.js on Vercel |
| Keyword data | Semrush API | Called from backend |
| Analytics | Vercel Analytics API + GSC API | Pulled by backend cron |

## Cost at Scale

| Service | Free Tier | Paid | At 50 Operators |
|---|---|---|---|
| Claude API | — | $3/M input, $15/M output tokens | ~$50-100/mo (10 articles/mo) |
| Semrush API | — | Existing plan covers it | $0 extra |
| Supabase | 500MB, 50K rows | $25/mo | $25/mo |
| Vercel | Free tier | $20/mo Pro | $20/mo |
| **Total** | | | **~$100-150/mo** |

Each article costs approximately $1-3 in Claude API calls. At $50-100/article to operators, the margins are 95%+.

## Migration Path (Current → Production)

### Step 1 (Now): Manual via Claude Code
```
You run agents → articles published → prove it works
```

### Step 2: Semi-automated via API
```
Dashboard shows keywords → You click "write" → Backend calls Claude API → auto-publishes
```

### Step 3: Fully automated
```
Keyword approved in dashboard → pipeline runs automatically → operator sees published article
```

Each step builds on the previous. No need to build everything at once.
