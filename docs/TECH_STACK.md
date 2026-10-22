# Tech Stack

## Services and accounts

| Service | Role | What you need | Cost |
|---|---|---|---|
| **Slack** | Where the SDR works | Your existing `@icp-bot` app, switched to **Socket Mode**: a bot token `xoxb-…` and an app-level token `xapp-…` | Free |
| **Supabase** | Source of truth (Postgres) | A project, plus its URL and **service_role** key | Free tier |
| **Deepline** | Enrichment: person, company, email waterfall, phone, people search | An API key (workspace bearer key) | Pay per lookup. Use BYOK (your own provider keys, no platform fee) or managed credits |
| **Anthropic (Claude)** | Research summary, colleague fit scores, LinkedIn drafts | An API key | Pay per token |
| **HubSpot** | CRM for the sales team | A Private App token with contacts, companies, notes and calls scopes | Free tier |
| **HeyReach** | LinkedIn sequences and sending messages | An API key, two campaigns (no-answer, post-call) and one LinkedIn sender | Paid |
| **Instantly** | Email sequences | An API v2 key and one campaign | Paid |

Build in order and only sign up when you reach the phase that needs a service: HubSpot in Phase 3, HeyReach and Instantly in Phase 4.

## Python tooling

| Tool | Why |
|---|---|
| **Python 3.12** | Current, well supported by every library below |
| **uv** | Installs Python and dependencies, manages the virtual environment and lock file, all with one fast tool (`uv sync`, `uv run`) |
| **ruff** | Linting and formatting in one tool |
| **pytest** + **pytest-mock** | Tests |
| **respx** | Fakes HTTP responses for `httpx` in tests, so no real API calls and no credits spent |
| **pre-commit** | Runs ruff and the fast tests before each commit |
| **mypy** (optional) | Type checking. Turn it on once the code settles |

## Libraries

| Library | Used for |
|---|---|
| `slack-bolt` | Slack listeners (mentions, buttons, modals) and Socket Mode |
| `slack-sdk` | Slack Web API calls (`chat.postMessage`, `chat.update`, `views.open`). Comes with Bolt |
| `supabase` | Supabase database access |
| `hubspot-api-client` | HubSpot's official SDK |
| `httpx` | HTTP client for Deepline, HeyReach and Instantly, which have no Python SDK |
| `tenacity` | Retries with backoff on rate limits and server errors |
| `anthropic` | Claude's official SDK. Uses `client.messages.parse(..., output_format=PydanticModel)` for validated structured outputs |
| `pydantic` / `pydantic-settings` | Data models; loads and validates settings from `.env` |
| `apscheduler` | Scheduled jobs: stuck-lead sweep every 10 min, daily summary, 90-day cleanup |

## Claude model

- **Model:** `claude-opus-5-5`, Anthropic's current default. It's one setting (`CLAUDE_MODEL` in `.env`), so you can switch any time after looking at cost.
- **Effort:** `low` for all three tasks. They're short, well-defined jobs, and low effort keeps them fast and cheap.
- **Structured outputs:** Pydantic models for:
  - `Research` (summary, talking points, icp_fit)
  - `FitScore` (score, reason)
  - `LinkedInDraft` (message)
- **Refusal fallback:** the SDK's server-side fallback (`fallbacks: "default"`) is turned on, so a rare safety refusal retries on a suitable model instead of failing the step.
- **Cost:** a few cents per lead at most. You'll measure it in the Phase 0 spike.

## Deepline: how the app talks to it

There's no Python SDK, so the app uses Deepline's REST API through `httpx`:

| Call | Endpoint |
|---|---|
| Read a tool's input contract (free) | `GET https://code.deepline.com/api/v2/integrations/{toolId}/get` |
| Run a tool | `POST https://code.deepline.com/api/v2/integrations/{toolId}/execute` with `{"payload": {...}}` |
| Start a prebuilt Play (e.g. `prebuilt/person-linkedin-to-email`) | `POST https://code.deepline.com/api/v2/plays/run` |
| Check a Play's result | `GET https://code.deepline.com/api/v2/runs/{run_id}`, polled until `completed` / `failed` |

Authentication is `Authorization: Bearer <DEEPLINE_API_KEY>`.

**To confirm in the Phase 0 spike**, before building on it:
1. The exact tool IDs for person enrichment, company enrichment, phone and people search.
2. Whether LinkedIn **follower and connection counts** are available. Some providers don't return them.
3. **Phone coverage.** One comparison says Deepline's phone waterfall was "coming soon", though phone providers such as Lusha are listed.
4. Cost per lead, and rate limits.

## Hosting

| Stage | Where |
|---|---|
| Building (Phases 0–6) | Your Mac: `uv run sdr-agent`. Socket Mode needs no ngrok |
| Always on (Phase 7) | **Railway** or Fly.io, as a single worker built from the `Dockerfile`. No inbound port is needed, about $5/month |

## Environment variables (`.env.example`)

```bash
# Slack (Socket Mode)
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...
SLACK_SIGNING_SECRET=...        # not needed for Socket Mode; kept for a possible HTTP mode later

# Supabase
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=...

# Deepline
DEEPLINE_API_KEY=...

# Claude
ANTHROPIC_API_KEY=...
CLAUDE_MODEL=claude-opus-5-5

# HubSpot (Phase 3)
HUBSPOT_TOKEN=...

# HeyReach + Instantly (Phase 4)
HEYREACH_API_KEY=...
HEYREACH_LINKEDIN_ACCOUNT_ID=...
HEYREACH_NO_ANSWER_CAMPAIGN_ID=...
HEYREACH_POST_CALL_CAMPAIGN_ID=...
INSTANTLY_API_KEY=...
INSTANTLY_CAMPAIGN_ID=...

# Behaviour
EXPANSION_MAX_PEOPLE=8
EXPANSION_REPEAT_DAYS=30
PHONE_LOOKUP_MIN_SENIORITY=manager   # skip pricey phone lookups below this
LOG_LEVEL=INFO
```
