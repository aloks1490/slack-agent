# SDR Intake + Lead Card: setup

Workflow file: [sdr-intake-lead-card.json](sdr-intake-lead-card.json)

## What it does

**Part A: someone types `@icp-bot <linkedin link>`**
1. **Clean URL** turns any version of the link into one standard form.
2. **Bad link:** reply in the thread with "That doesn't look like a LinkedIn profile link".
3. **Already in Supabase:** post the lead card in the thread, with "Already in the pipeline, owner, status" and a link to the original thread.
4. **New person:**
   - save a row in Supabase (`received`)
   - reply "Enriching…" in the thread
   - send `lead_id` + `linkedin_url` to Clay
   - set the status to `enriching`

**Part B: Clay sends the enriched person back**
1. Tidy the fields and save them to Supabase (`enriched`).
2. Post the lead card in that lead's thread.

**The lead card shows:**
- name, title, company, email, phone, location, company size, industry, followers and connections
- the research summary and talking points
- buttons: **Picked up**, **Did not pick up**, **Wrong person** and **LinkedIn**

The call buttons show up, but clicking them does nothing yet. That's the next workflow.

---

## 1. Supabase (10 min)

1. Create a free project at supabase.com.
2. Open **SQL Editor → New query**, paste all of [supabase-schema.sql](supabase-schema.sql) and click **Run**.
3. Open **Project Settings → API** and copy:
   - the **Project URL**
   - the **service_role** key (secret)

## 2. n8n (10 min)

1. Import the workflow: **Create workflow → ⋯ → Import from file → sdr-intake-lead-card.json**.
2. Create two credentials:
   - **Supabase API**: Host = Project URL, Service Role Secret = service_role key
   - **Slack API**: Access Token = your bot token `xoxb-…`
3. Pick the credential in each node that shows a warning:
   - **Slack API:** `Slack Trigger`, `Slack: invalid link`, `Slack: enriching`, `Slack: post lead card`
   - **Supabase API:** every node whose name starts with `Supabase:`
4. Fill in the two **Config** nodes:
   - `Config`: Supabase URL + your Clay table's webhook URL
   - `Config (results)`: the same Supabase URL
5. **Publish** the workflow.
6. Deactivate your old workflow. Otherwise both react to every `@icp-bot` mention.

## 3. Slack (5 min)

At api.slack.com/apps, open your app:
1. **Event Subscriptions:**
   - set **Request URL** to the `Slack Trigger` production URL, `https://passive-deed-primarily.ngrok-free.dev/webhook/<id>/webhook`
   - wait for **Verified ✓**
   - check that `app_mention` is under bot events
   - click **Save**
2. **OAuth & Permissions:** the bot needs `app_mentions:read` and `chat:write`. If you add a scope, reinstall the app.
3. Invite the bot to your channel: `/invite @icp-bot`.

## 4. Clay (30–60 min)

Your existing table already receives the link. Two changes:

**a. Inputs.** The webhook now sends `lead_id` and `linkedin_url`. Map both into columns. `lead_id` is new, and it's how n8n knows which Supabase row the results belong to.

**b. Enrichment columns**, if you don't have them yet:
- Enrich person from LinkedIn profile
- Enrich company
- Email waterfall + validation
- Phone waterfall
- An AI column for research

**c. A final HTTP API column:**
- **Method:** POST
- **URL:** `https://passive-deed-primarily.ngrok-free.dev/webhook/clay-enriched`
- **Body:** JSON. Type `/` to insert each Clay column, and leave out any you don't have:
  ```json
  {
    "lead_id": "/lead_id",
    "first_name": "/First Name",
    "last_name": "/Last Name",
    "full_name": "/Full Name",
    "title": "/Title",
    "headline": "/Headline",
    "location": "/Location",
    "company_name": "/Company Name",
    "company_domain": "/Company Domain",
    "company_linkedin_url": "/Company LinkedIn URL",
    "company_size": "/Company Size",
    "industry": "/Industry",
    "work_email": "/Work Email",
    "email_status": "/Email Status",
    "phone": "/Phone",
    "linkedin_followers": "/Followers",
    "linkedin_connections": "/Connections",
    "research_summary": "/Research Summary",
    "talking_points": "/Talking Points"
  }
  ```
  - The key names on the left must stay exactly as shown. They match the Supabase columns.
  - The research fields can be plain text or a list.
  - If your AI column returns one object like `{ "summary": [...], "talking_points": [...] }`, send it as `"research": "/AI Research"` instead of the last two lines.
- **Run condition:** only run once the email and AI columns are filled, so it fires once with complete data.

## 5. Test

| In Slack | Expected |
|---|---|
| `@icp-bot https://www.linkedin.com/in/<real person>` | "Enriching…" in the thread → Supabase row `enriching` → Clay row → lead card in the thread a few minutes later, Supabase row `enriched` |
| Same link again (or with `?utm_source=x`) | Lead card straight away, with "Already in the pipeline" |
| `@icp-bot hello` | "That doesn't look like a LinkedIn profile link" |

## If something breaks

- **Nothing happens in n8n:** check that Docker and ngrok are running, the workflow is **Published**, and the Slack Request URL is verified.
- **No reply in Slack:** the bot isn't in the channel, or the bot token is missing the `chat:write` scope. Open the failed run in **Executions** and look at the red node.
- **Supabase 401:** wrong key. Make sure it's the service_role key, not the anon key.
- **Clay row never comes back:** check the HTTP API column's URL and run condition. Clay can only reach n8n while ngrok is running.
