# Slack SDR Agent

An SDR mentions `@icp-bot` with a LinkedIn link in Slack. A couple of minutes later, a lead card appears in the thread with:
- email, phone, company details
- a research summary and talking points
- buttons for the call outcome

It also saves everything in Supabase and HubSpot, starts follow-up sequences when nobody picks up, finds other people to call at the same company, and drafts the follow-up message after a call. The SDR approves every message before it goes out.

**Stack:** Python · Slack (Bolt, Socket Mode) · Deepline · Claude · Supabase · HubSpot · HeyReach · Instantly

## How it works, in plain words

1. **Mention the bot with a link.** The bot cleans the link and checks Supabase.
2. **Already known?** The lead card appears in the thread right away.
3. **New person?** The bot saves them, looks them up through Deepline (profile, company, email, phone), has Claude write a short research summary, saves it all, adds them to HubSpot and posts the lead card.
4. **The SDR calls and presses a button:**
   - **Did not pick up:** the lead goes into LinkedIn (HeyReach) and email (Instantly) sequences, and the bot suggests up to 8 more people at the same company.
   - **Wrong person:** marked as not a fit, plus the same colleague suggestions.
   - **Picked up:** the SDR types call notes, Claude drafts a LinkedIn message, the SDR edits or approves it, and it's sent through HeyReach.

## Docs

| Doc | What's in it |
|---|---|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | The pieces, the flows, lead statuses, key decisions |
| [docs/IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md) | 8 phases, each with tasks and a pass/fail gate |
| [docs/TESTING.md](docs/TESTING.md) | Test layers, the cases to cover, and the Slack checklist |
| [docs/TECH_STACK.md](docs/TECH_STACK.md) | Services, libraries, Claude setup, Deepline API, env vars |

To see the diagrams rendered, open `diagrams.html` in the in-app browser.

## Repo structure

```
slack-sdr/
├── README.md
├── pyproject.toml              # dependencies + ruff/pytest config (managed by uv)
├── uv.lock
├── .python-version             # 3.12 (uv installs it)
├── .env.example                # every setting, no secrets (copy to .env)
├── .gitignore
├── .pre-commit-config.yaml
├── Dockerfile                  # Phase 7: deploy as one worker
├── .github/workflows/ci.yml    # lint + fast tests on every push
│
├── docs/                       # architecture, plan, testing, stack, deepline-findings
├── db/
│   └── migrations/
│       └── 001_initial_schema.sql
│
├── src/sdr_agent/
│   ├── main.py                 # entry point: Slack Socket Mode + scheduler
│   ├── config.py               # settings loaded from .env (pydantic-settings)
│   │
│   ├── domain/                 # pure logic, no network calls
│   │   ├── models.py           #   Lead, CallOutcome, Research, FitScore…
│   │   ├── statuses.py         #   lead statuses + allowed transitions
│   │   └── linkedin.py         #   link cleaning
│   │
│   ├── clients/                # one thin wrapper per external API
│   │   ├── supabase_repo.py
│   │   ├── deepline.py
│   │   ├── hubspot.py
│   │   ├── heyreach.py
│   │   ├── instantly.py
│   │   └── llm.py              #   Claude: research, fit score, drafts
│   │
│   ├── services/               # business logic, no Slack code
│   │   ├── intake.py           #   mention → dedupe → save
│   │   ├── enrichment.py       #   Deepline + Claude → Supabase
│   │   ├── crm_sync.py         #   → HubSpot
│   │   ├── outreach.py         #   no answer / wrong person → sequences
│   │   ├── expansion.py        #   colleagues at the same company
│   │   └── messaging.py        #   call notes → draft → send
│   │
│   ├── slack/
│   │   ├── app.py              # Bolt app + listener registration
│   │   ├── handlers/           # thin: ack, then hand work to services/jobs
│   │   │   ├── mentions.py
│   │   │   ├── call_buttons.py
│   │   │   ├── modals.py
│   │   │   ├── expansion_buttons.py
│   │   │   └── retry.py        #   Retry button on failure alerts
│   │   └── blocks/             # Block Kit builders (pure functions)
│   │       ├── lead_card.py
│   │       ├── expansion_card.py
│   │       ├── draft_card.py
│   │       └── call_notes_modal.py
│   │
│   ├── jobs/
│   │   ├── runner.py           # background thread pool + error handling
│   │   └── scheduled.py        # stuck-lead sweep, daily summary, cleanup
│   │
│   └── prompts/                # Claude prompts as plain text files
│       ├── research.md
│       ├── fit_score.md
│       └── linkedin_message.md
│
├── tests/
│   ├── conftest.py             # fake clients + shared fixtures
│   ├── test_smoke.py           # package imports (keeps CI green early on)
│   ├── fixtures/               # recorded Deepline/HubSpot/Slack payloads
│   ├── unit/
│   ├── integration/
│   ├── contract/
│   ├── live/                   # real APIs, run by hand (pytest -m live)
│   └── llm/                    # Claude output checks (pytest -m llm)
│
├── scripts/
│   └── deepline_spike.py       # Phase 0: try every Deepline tool on real profiles
│
└── archive/n8n-clay/           # the earlier n8n + Clay version, for reference
```

**The one rule that keeps it tidy:** handlers → services → clients. Handlers only talk to Slack. Services hold the logic and never import Slack. Clients only talk to one API each.

## Getting started

Once Phase 0 is built:

```bash
uv sync
```
```bash
cp .env.example .env
```
Fill in `.env`, then:
```bash
uv run sdr-agent
```
```bash
uv run pytest
```

## Status

Skeleton created: every file says what it's for and what goes in it, but no logic yet. Next: **Phase 0**, which covers the Slack Socket Mode hello-world and the Deepline check. See the [implementation plan](docs/IMPLEMENTATION_PLAN.md).
