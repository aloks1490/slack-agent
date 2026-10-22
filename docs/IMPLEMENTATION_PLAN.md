# Implementation Plan

Eight phases. **Don't start the next phase until the current one's gate passes with a real LinkedIn profile.** Each phase ends with a commit.

| Phase | What you get | Time (part-time) |
|---|---|---|
| 0 | Repo set up, bot replies in Slack, Deepline checked | 1–2 days |
| 1 | Intake: mention → clean → dedupe → save → thread reply | 1 day |
| 2 | Enrichment + research + lead card with buttons | 2–3 days |
| 3 | HubSpot sync | 1–2 days |
| 4 | Did not pick up + Wrong person → HeyReach + Instantly | 2 days |
| 5 | Account expansion | 2 days |
| 6 | Picked up → notes → AI draft → send | 2 days |
| 7 | Hardening, reporting, deploy | 2–3 days |

Phases 0–2 match what you first scoped: mention → Supabase check → enrich → save → card with three buttons.

---

## Phase 0: Setup and Deepline check

**Goal:** a working repo, a bot that answers in Slack, and facts about Deepline instead of guesses.

1. **Repo skeleton.** Create `pyproject.toml` (uv), the `src/sdr_agent/` layout from the README, `.env.example`, ruff and pytest config, and pre-commit.
2. **Supabase.** Create the project and run `db/migrations/001_initial_schema.sql`, which adds the five tables plus `sdr_owners`.
3. **Slack app → Socket Mode.** In your `@icp-bot` app:
   - turn on **Socket Mode** and create an app-level token (`connections:write`)
   - under **Event Subscriptions**, subscribe to `app_mention`
   - turn on **Interactivity**
   - bot scopes: `app_mentions:read`, `chat:write`, `users:read`, `users:read.email`, then reinstall
   - deactivate the old n8n workflow
4. **Hello world.** `main.py` starts Bolt in Socket Mode. On `app_mention`, it replies "pong" **in a thread** under the message.
5. **Deepline spike** (`scripts/deepline_spike.py`). Run it against 3–5 real profiles. For each, try:
   - the person-from-LinkedIn tool
   - company enrichment
   - the email waterfall Play
   - a phone tool
   - people search on the person's company domain

   Save every raw response to `tests/fixtures/deepline/` (these become your test data). Write the results into a table in `docs/deepline-findings.md`, covering:
   - which fields came back (title, followers, connections, email, phone…)
   - the hit rate, the time taken and the cost per call
6. **Decide** based on the findings:
   - which tool IDs to use
   - whether followers and connections are available (if not, drop them from the card or add a provider)
   - the phone strategy

**Gate:** "pong" appears in a thread; Supabase has the tables; `deepline-findings.md` exists with real numbers.

---

## Phase 1: Intake

**Goal:** a mention creates exactly one lead and one thread, and never a duplicate.

1. `domain/linkedin.py`: `normalise(text) -> str | None`, with unit tests for every link variant (tracking codes, trailing slash, mobile, `mwlite`, Slack's `<url|label>` wrapping, company pages, Sales Navigator).
2. `clients/supabase_repo.py`: `find_lead_by_url`, `create_lead`, `update_lead`, `get_lead`.
3. `services/intake.py`: `handle_mention(text, user, channel, ts, thread_ts)` returns one of `Invalid` / `Existing(lead)` / `Created(lead)`.
4. `slack/handlers/mentions.py`: calls the service and replies in the thread. For `Existing`, it posts a simple lead card with "Already in the pipeline · owner · status · original thread".
5. Check `do_not_contact` before doing anything for an existing lead.

**Gate:**
- a new link gives one Supabase row (`received`) and an "Enriching…" reply in the thread
- the same link again, or with `?utm_source=`, gives "Already in the pipeline" and no new row
- a company page gives the "not a profile link" reply

---

## Phase 2: Enrichment and the lead card

**Goal:** a full lead card in the thread within about 3 minutes.

1. `clients/deepline.py`: `execute_tool(tool_id, payload)` and `run_play(name, input, timeout)`, which polls with backoff. Retries come from tenacity. Responses are mapped into Pydantic models using the Phase 0 fixtures.
2. `clients/llm.py`: `research(lead) -> Research` via `messages.parse`. The prompt lives in `prompts/research.md`, grounded only in the enrichment data: "If data is missing, say so."
3. `services/enrichment.py`: the pipeline from ARCHITECTURE flow 2:
   - each step is a function, and a failed step records what's missing and carries on
   - phone lookup only above `PHONE_LOOKUP_MIN_SENIORITY`
   - saves to Supabase with status `enriched`
4. `jobs/runner.py`: a thread pool and `submit(job, lead_id)`. On an exception it:
   - writes a `workflow_errors` row
   - sets the lead to `error`
   - posts "Something failed at <step>" in the thread with a **Retry** button
5. `slack/blocks/lead_card.py`:
   - header, then fields (title, company, email + status, phone, location, size, industry, followers, connections, status)
   - research and talking points, plus a "No phone found, start on LinkedIn" hint when there's no phone
   - buttons: **Picked up · Did not pick up · Wrong person · LinkedIn**
   - button clicks just reply "coming soon" until Phase 4
6. Wire it up: intake `Created` → `runner.submit(enrich, lead_id)` → post the card when done.

**Gate:**
- a real profile gets a card in under 3 minutes and a Supabase row with status `enriched`, every field filled where data exists
- a profile with no email or no phone still gets a card that says so

---

## Phase 3: HubSpot sync

1. `clients/hubspot.py`: search company by domain → create if missing; search contact by email, then by `linkedin_url` → create or update; associate; add a note. Add the custom properties: `linkedin_url`, `linkedin_followers`, `linkedin_connections`, `research_summary`.
2. `sdr_owners` table: Slack user ID → HubSpot owner ID. Set the owner on create, and don't overwrite an existing owner without saying so in the card.
3. `services/crm_sync.py` runs after enrichment: saves the IDs and sets status `in_crm`. The card shows a HubSpot link.

**Gate:** one correctly owned and associated contact and company per lead, with the note attached; running the same lead again updates rather than duplicates.

---

## Phase 4: Did not pick up and Wrong person

1. `slack/handlers/call_buttons.py`: `ack()` first, then hand off to the job runner.
2. `services/outreach.py`, `no_answer(lead_id, sdr)`:
   - **idempotency:** if `outreach_events` already has `heyreach_enrolled` for this lead → reply "Already sequenced" and stop
   - log the call (`call_logs`) and set status `called_no_answer`
   - run in parallel: HeyReach `AddLeadsToCampaignV2` (no-answer campaign, with `talking_point` as a custom variable), and Instantly create-lead (only if the email is valid; otherwise log "email skipped")
   - write the `outreach_events` rows, set status `sequenced`, log the call in HubSpot
   - `chat.update` the card: "Did not pick up: enrolled in LinkedIn + email by @sdr at 11:52"
3. `wrong_person(lead_id, sdr)`: log it, set status `disqualified`, update the card.
4. Both then call `expansion.start(lead_id)`, which is a stub until Phase 5.

**Gate:** one click enrols the lead once in both tools and logs it in Supabase and HubSpot; a fast double-click changes nothing; with no valid email, HeyReach still runs and the card explains why email was skipped.

---

## Phase 5: Account expansion

1. Persona config in `config.py` or a Supabase `personas` table: target titles, departments and seniority, plus excluded titles (interns, recruiters…).
2. `services/expansion.py`, `start(lead_id)`:
   - if the same `company_domain` was searched in the last 30 days → post "Already searched <company> on <date>" with a link, and stop
   - create an `expansion_runs` row with status `searching`
   - Deepline people search with the persona filter, max 8
   - drop the original person and anyone already in `leads`
   - light enrichment (email only, no phone) and a Claude `FitScore` (1–5 + a one-line reason)
   - insert as `suggested`, with `parent_lead_id` and `fit_reason`
   - post one expansion card sorted by fit, and set the run to `posted`
   - zero people → "No other matching people found", run `empty`
3. `slack/handlers/expansion_buttons.py`:
   - **Add as lead** → status `received` → the full enrichment job, which includes a phone lookup and posts a card in the same thread
   - **Skip** → status `skipped`, greyed out on the card

**Gate:** one *Did not pick up* gives, within about 5 minutes, one expansion card with up to 8 relevant people (never the original person, never a duplicate); *Add as lead* gives a full card for that person in the same thread.

---

## Phase 6: Picked up → AI draft → send

1. **Picked up:** call `views.open` **first**, because the `trigger_id` expires in 3 seconds. The form includes the call outcome, notes and the message goal; `private_metadata` holds the `lead_id`. Cancelling the form logs nothing.
2. **Form submitted:**
   - log the call and set status `called_connected`, then log it in HubSpot with the notes
   - *Not interested* → close out, no draft
3. `clients/llm.py`, `draft_message(...) -> LinkedInDraft`. Rules:
   - under 300 characters
   - mention one specific thing from the call
   - one clear next step
   - no emojis
   - never invent facts

   Post the draft with **Send via HeyReach · Edit · Regenerate · Copy, I'll send it**, and set status `message_drafted`.
4. **Edit** → a modal pre-filled with the draft → replaces it. **Regenerate** → a new draft, different from the last. **Send** → HeyReach post-call campaign with `custom_message`, status `message_sent`, a HubSpot note with the exact text, card updated. **Copy** → show the text in a code block, logged as `manual`.

**Gate:** Picked up → notes → a draft in the thread within 15 s that reflects the call accurately; Send puts it in HeyReach, and Supabase, HubSpot and Slack all show the same status.

---

## Phase 7: Hardening, reporting, deploy

1. **Retries:** tenacity on every client (3 tries, exponential backoff, only for 429 and 5xx).
2. **Sweeper** (APScheduler, every 10 min):
   - leads in `enriching` for more than 15 min → retry once, then alert in the thread
   - expansion runs in `searching` for more than 10 min → post whatever's there
3. **Cleanup:** delete `skipped` suggestions after 90 days.
4. **Reporting:** Supabase views for leads per SDR per day, connect rate, sequenced count, suggestions added vs skipped and messages sent, plus a daily summary posted to Slack.
5. **Deploy:** a `Dockerfile`, then a Railway worker with the env vars set in Railway. Run only **one** instance (Socket Mode).
6. **Docs and demo:** update the README and record a 5–7 min Loom of the full flow.

**Gate:** kill the Deepline key on purpose → you get an alert in the thread, a `workflow_errors` row, and Retry works once the key is restored.

---

## Stretch goals (later)

- Pause sequences when the prospect replies (HeyReach and Instantly webhooks → this needs a public URL, so reuse your ngrok domain or the Railway URL)
- A **Find more people** button on every card
- `@icp-bot company <domain>`: start from an account, get the buying committee
- Personas editable in Supabase without a code change
- Upload a call recording → AI summary instead of typed notes
- A weekly SDR leaderboard
