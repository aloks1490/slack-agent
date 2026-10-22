# Testing Plan

## The idea

Most tests never touch a real API. Services get **fake clients**, and HTTP clients get **recorded responses** (saved during the Phase 0 Deepline spike). That keeps the test suite fast and free, so you can run it on every save. A small, separate set of **live** tests hits the real APIs on purpose, run by hand.

| Layer | What's tested | Real APIs? | When it runs |
|---|---|---|---|
| **Unit** | Pure logic: link cleaning, status rules, card builders, response mappers, prompt builders | No | Every commit (pre-commit) |
| **Integration** | Services end to end with fake clients: the whole flow's decisions | No | Every commit |
| **Contract** | Client code against recorded real responses | No (recorded) | Every commit |
| **Live** (`pytest -m live`) | Each client against the real API with one test profile | **Yes, costs credits** | By hand, after changing a client |
| **AI checks** (`pytest -m llm`) | Claude outputs against fixed inputs, checked against the rules | **Yes, costs tokens** | By hand, after changing a prompt |
| **End to end in Slack** | The full checklist below | Yes | End of every phase |

**Commands:**
```bash
uv run pytest
```
```bash
uv run pytest -m live
```
```bash
uv run pytest -m llm
```
The first runs unit, integration and contract tests. The other two are the paid suites.

---

## Unit tests (`tests/unit/`)

| Module | Cases |
|---|---|
| `domain/linkedin.py` | A normal link; uppercase; trailing slash; `?utm_source=`; `m.linkedin.com`; `/mwlite/in/`; Slack `<url>` and `<url\|label>`; a mention token before the link; a company page → `None`; Sales Navigator → `None`; empty text → `None`; two links → the first profile |
| `domain/statuses.py` | Allowed transitions pass (`received → enriching`…); illegal ones raise (`sequenced → received`); `do_not_contact` blocks outreach |
| `slack/blocks/lead_card.py` | All fields → expected blocks (snapshot); missing phone → hint shown; `do_not_contact` → no buttons; "already in pipeline" note; **Block Kit limits**: ≤ 10 fields per section, header ≤ 150 chars, section text ≤ 3000, ≤ 50 blocks; button `value` = lead ID |
| `slack/blocks/expansion_card.py` | Sorted by fit; ≤ 8 people; Add/Skip carry the right IDs; skipped people are greyed out |
| `clients/deepline.py` mappers | Each recorded response → the right Pydantic model; missing fields → `None`, never a crash; number strings like `"12,345"` → `12345` |
| `clients/llm.py` prompt builders | The prompt includes only the given data; missing data is labelled "not available" |

## Integration tests (`tests/integration/`)

Services run with in-memory fakes (`FakeRepo`, `FakeDeepline`, `FakeHubSpot`, `FakeHeyReach`, `FakeInstantly`, `FakeLLM`, `FakeSlack`). Each fake records the calls made to it, so a test can assert *what was sent where*.

**Intake**
- New link → one lead `received`, one "Enriching…" reply in the right thread, one enrichment job submitted
- Same link twice → one lead; the second time posts the "already" card
- The same person through different link variants → one lead
- Invalid link → reply only, nothing saved
- `do_not_contact` lead → blocked message, no card buttons

**Enrichment**
- Full data → lead `enriched` then `in_crm`, card posted with every field
- No email found → card says "Not found", pipeline continues
- No phone → hint on the card; a junior title → phone lookup **not called**
- Deepline 500 on the company step → retried, then carries on without company data
- Uncaught crash → `workflow_errors` row, status `error`, alert with Retry in the thread
- Retry → runs again from the start, and succeeds

**HubSpot**
- Existing company by domain → reused, not duplicated
- Existing contact by email → updated; owner kept, with a warning on the card
- No email → matched by `linkedin_url`

**Outreach**
- No answer → HeyReach + Instantly called once each, two `outreach_events`, status `sequenced`, HubSpot call logged, card updated
- **Double click** (two calls straight after each other) → enrolled exactly once
- Invalid email → HeyReach only, "email skipped" logged
- Wrong person → `disqualified`, expansion started

**Expansion**
- Returns 8 people including the original person and one existing lead → card shows 6
- Zero people → "No other matching people found", run `empty`
- Same domain searched 10 days ago → no Deepline call, link to the old thread
- Add as lead → status `received`, full enrichment submitted **with** phone lookup
- Skip → `skipped`; never enrolled anywhere

**Picked up**
- Modal opened before any other work (assert call order)
- Not interested → call logged, no draft
- Draft → Send → HeyReach post-call campaign called with the exact text, status `message_sent`, HubSpot note
- Regenerate → the LLM is asked for a different draft (previous draft included in the request)

## Contract tests (`tests/contract/`)

Use **respx** to replay the recorded Deepline, HubSpot, HeyReach and Instantly responses through the real client code. These catch bugs in request building and response parsing without spending credits. When a vendor changes their API, record a new fixture with the live suite and update the mapper.

## Live tests (`tests/live/`, marked `live`)

- One known public test profile, run through each Deepline tool → asserts the shape of the result, not exact values
- HubSpot: create, then delete a test contact
- HeyReach and Instantly: run against a **test campaign**, never a real one
- These are skipped automatically if the needed env vars aren't set

## AI checks (`tests/llm/`, marked `llm`)

A small fixed set of inputs, with rules checked in code:

| Output | Inputs | Checks |
|---|---|---|
| Research | 5 recorded enrichment payloads (one with almost no data) | Exactly 3 talking points; every company or role mentioned appears in the input; for the empty payload, says data is missing rather than guessing |
| Fit score | 6 people against one persona | Score 1–5; reason ≤ 120 chars; an intern or recruiter scores ≤ 2 |
| LinkedIn draft | 8 call-note samples, including a one-word note | ≤ 300 chars; no emojis; no "I hope this finds you well"; has a next step; for the one-word note, stays generic and adds no new facts |

Read the outputs yourself too: the code checks catch rule breaks, and your own read catches tone.

---

## End-to-end checklist in Slack

Run at the end of each phase, ticking the cases that phase covers. This list comes from the original project doc.

- [ ] A normal profile with email and phone → full flow, both call outcomes
- [ ] The same link twice, and by two different SDRs → no duplicate rows, contacts or enrolments
- [ ] A link with tracking codes, a trailing slash or a mobile link → one row
- [ ] A company page or Sales Navigator link → friendly error, nothing created
- [ ] No email found → card posts; Did not pick up skips Instantly and says why; HeyReach still runs
- [ ] No phone → the card says so; Did not pick up still starts LinkedIn follow-up and expansion
- [ ] Contact already in HubSpot → updated, not duplicated; owner not overwritten silently
- [ ] Did not pick up clicked twice quickly → enrolled once, one expansion run
- [ ] Expansion finds nobody → a clear "no other matching people" message
- [ ] Expansion returns the original person or an existing lead → they're left off the card
- [ ] Two SDRs on the same company in the same month → the second sees the earlier search, no new Deepline spend
- [ ] Add as lead → full lead card in the same thread, with a phone lookup
- [ ] Form opened, then cancelled → nothing logged
- [ ] One-word call notes → the draft stays generic and invents nothing
- [ ] HeyReach, Instantly, HubSpot or Deepline returns an error → alert in the thread; the lead shows `error`; Retry works

## Quality bar

- `uv run pytest` passes before every commit (pre-commit runs it)
- At least 80% coverage on `domain/` and `services/`. Clients are covered by the contract tests.
- Every bug found by hand gets a test that reproduces it before it's fixed
