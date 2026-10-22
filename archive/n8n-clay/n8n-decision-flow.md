# Slack SDR Agent: n8n Decision Flow

Each chart reads **left to right**, like an n8n canvas. Every box is one node, labelled `Node type` on top and what it does underneath. Diamonds are **IF** or **Switch** nodes, and their branches are labelled the way n8n labels them (`true` / `false`, or the Switch value).

| Colour | Node type |
|---|---|
| 🟧 Orange-red, rounded | Trigger (Webhook, Error Trigger, Schedule) |
| 🟩 Dark green diamond | IF / Switch logic |
| 🟢 Light green | Supabase |
| 🟪 Purple | Slack |
| 🟠 Orange | HubSpot |
| 🔵 Blue | HTTP Request to HeyReach / Instantly / Clay |
| ⚫ Grey | Code, Respond, AI and other utility nodes |
| ▭ Double-edged box | Execute Sub-workflow |

---

## 0. The map: how the pieces hand off

Start here. Only **three things** ever start work: the `/prospect` command, a Slack button or modal, and Clay posting results back.

```mermaid
flowchart LR
    classDef trigger fill:#FF6D5A,color:#fff,stroke:#E5533F
    classDef wf fill:#1F2937,color:#fff,stroke:#111827
    classDef clay fill:#F5C542,color:#000,stroke:#C9A227
    classDef slack fill:#4A154B,color:#fff,stroke:#4A154B

    T1(["/prospect command"]):::trigger --> WF1["WF1 Intake"]:::wf
    WF1 --> C1["Clay Table 1<br/>enrich person"]:::clay
    C1 --> WF2["WF2 Sync"]:::wf
    WF2 --> CARD["Lead card<br/>3 buttons"]:::slack

    CARD -->|"SDR clicks"| T2(["Slack button or modal"]):::trigger
    T2 --> WF3["WF3 Actions"]:::wf

    WF3 -->|"No answer or<br/>Wrong person"| C2["Clay Table 2<br/>find colleagues"]:::clay
    C2 --> WF5["WF5 Expansion"]:::wf
    WF5 --> ECARD["Expansion card<br/>Add / Skip"]:::slack
    ECARD -->|"SDR clicks Add"| T2
    WF3 -->|"Add as lead"| C1

    WF3 -->|"Picked up"| MSG["AI draft, SDR approves,<br/>sent via HeyReach"]:::slack

    WF4["WF4 Errors<br/>watches all workflows"]:::wf
```

---

## 1. WF1 Intake

**Trigger:** the SDR types `/prospect <linkedin-url>`.

```mermaid
flowchart LR
    classDef trigger fill:#FF6D5A,color:#fff,stroke:#E5533F
    classDef logic fill:#2E7D5B,color:#fff,stroke:#1F5E43
    classDef db fill:#3ECF8E,color:#000,stroke:#2DA36F
    classDef slack fill:#4A154B,color:#fff,stroke:#4A154B
    classDef http fill:#2D6CDF,color:#fff,stroke:#1F4FA8
    classDef util fill:#6B7280,color:#fff,stroke:#4B5563

    A(["Webhook<br/>POST /sdr-intake"]):::trigger
    B["Respond to Webhook<br/>Got it, enriching now"]:::util
    C["Code<br/>Normalise URL"]:::util
    D{"IF<br/>URL valid?"}:::logic
    D0["Slack<br/>Error: paste a profile URL"]:::slack
    E["Supabase<br/>Get lead by URL"]:::db
    F{"IF<br/>Lead exists?"}:::logic
    F0["Slack<br/>Already in pipeline,<br/>owner + thread link"]:::slack
    G["Supabase<br/>Insert lead<br/>status = received"]:::db
    H["Slack<br/>Post thread message"]:::slack
    I["Supabase<br/>Save slack_thread_ts"]:::db
    J[["Sub-workflow<br/>Send to Clay Table 1"]]:::util

    A --> B --> C --> D
    D -->|false| D0
    D -->|true| E --> F
    F -->|true| F0
    F -->|false| G --> H --> I --> J
```

**The "Send to Clay Table 1" sub-workflow**, which WF1 and the *Add as lead* button both use:

```mermaid
flowchart LR
    classDef db fill:#3ECF8E,color:#000,stroke:#2DA36F
    classDef http fill:#2D6CDF,color:#fff,stroke:#1F4FA8
    classDef util fill:#6B7280,color:#fff,stroke:#4B5563

    S(["Execute Workflow Trigger<br/>lead_id, linkedin_url"]):::util
    K["HTTP Request<br/>POST Clay Table 1 webhook"]:::http
    L["Supabase<br/>status = enriching"]:::db
    S --> K --> L
```

---

## 2. Clay Table 1: Enrich person

This isn't n8n. It's a Clay table, read as columns left to right.

```mermaid
flowchart LR
    classDef clay fill:#F5C542,color:#000,stroke:#C9A227
    classDef logic fill:#2E7D5B,color:#fff,stroke:#1F5E43
    classDef http fill:#2D6CDF,color:#fff,stroke:#1F4FA8

    A["Webhook source<br/>lead_id, linkedin_url"]:::clay
    B["Enrich person<br/>name, title, followers,<br/>connections, company"]:::clay
    C["Enrich company<br/>size, industry, HQ"]:::clay
    D["Email waterfall<br/>+ validation"]:::clay
    E{"Run condition<br/>Senior enough?"}:::logic
    F["Phone waterfall"]:::clay
    G["AI column<br/>3-bullet summary +<br/>3 talking points"]:::clay
    H["Formula<br/>icp_fit yes or no"]:::clay
    I["HTTP API column<br/>POST to WF2<br/>only when complete"]:::http

    A --> B --> C --> D --> E
    E -->|yes| F --> G
    E -->|no| G
    G --> H --> I
```

---

## 3. WF2 Sync: CRM and lead card

**Trigger:** Clay Table 1 posts the enriched lead.

```mermaid
flowchart LR
    classDef trigger fill:#FF6D5A,color:#fff,stroke:#E5533F
    classDef logic fill:#2E7D5B,color:#fff,stroke:#1F5E43
    classDef db fill:#3ECF8E,color:#000,stroke:#2DA36F
    classDef slack fill:#4A154B,color:#fff,stroke:#4A154B
    classDef hub fill:#FF7A59,color:#fff,stroke:#E5603F
    classDef util fill:#6B7280,color:#fff,stroke:#4B5563

    A(["Webhook<br/>POST /sdr-enriched"]):::trigger
    B["Respond to Webhook<br/>200 OK"]:::util
    C["Supabase<br/>Save enrichment<br/>status = enriched"]:::db
    D["HubSpot<br/>Search company by domain"]:::hub
    E{"IF<br/>Company found?"}:::logic
    E1["HubSpot<br/>Create company"]:::hub
    F["HubSpot<br/>Search contact by email,<br/>else by linkedin_url"]:::hub
    G{"IF<br/>Contact found?"}:::logic
    G1["HubSpot<br/>Update contact"]:::hub
    G2["HubSpot<br/>Create contact<br/>set SDR as owner"]:::hub
    H["HubSpot<br/>Associate + add<br/>research note"]:::hub
    I["Supabase<br/>Save HubSpot IDs<br/>status = in_crm"]:::db
    J["Slack<br/>Post lead card:<br/>Picked up / No answer /<br/>Wrong person"]:::slack

    A --> B --> C --> D --> E
    E -->|false| E1 --> F
    E -->|true| F
    F --> G
    G -->|true| G1 --> H
    G -->|false| G2 --> H
    H --> I --> J
```

---

## 4. WF3 Actions: the router

**Trigger:** every Slack button click and modal submit arrives here. A Switch node sends each one to its branch, and each branch has its own chart below.

```mermaid
flowchart LR
    classDef trigger fill:#FF6D5A,color:#fff,stroke:#E5533F
    classDef logic fill:#2E7D5B,color:#fff,stroke:#1F5E43
    classDef util fill:#6B7280,color:#fff,stroke:#4B5563
    classDef branch fill:#fff,color:#111,stroke:#111,stroke-dasharray:4 3

    A(["Webhook<br/>POST /sdr-actions"]):::trigger
    B["Code<br/>JSON.parse payload"]:::util
    C["Respond to Webhook<br/>200 OK within 3s"]:::util
    D{"Switch<br/>action_id"}:::logic

    A --> B --> C --> D
    D -->|call_no_answer| N["4a No answer"]:::branch
    D -->|wrong_person| W["4b Wrong person"]:::branch
    D -->|"call_connected<br/>call_notes_submit"| P["4c Picked up"]:::branch
    D -->|"send / edit /<br/>regenerate / copy"| M["4d Draft buttons"]:::branch
    D -->|"add_suggested_lead<br/>skip_suggested_lead"| X["4e Expansion buttons"]:::branch
```

### 4a. No answer

```mermaid
flowchart LR
    classDef logic fill:#2E7D5B,color:#fff,stroke:#1F5E43
    classDef db fill:#3ECF8E,color:#000,stroke:#2DA36F
    classDef slack fill:#4A154B,color:#fff,stroke:#4A154B
    classDef hub fill:#FF7A59,color:#fff,stroke:#E5603F
    classDef http fill:#2D6CDF,color:#fff,stroke:#1F4FA8
    classDef util fill:#6B7280,color:#fff,stroke:#4B5563

    A["Supabase<br/>Find heyreach_enrolled<br/>for this lead"]:::db
    B{"IF<br/>Already enrolled?"}:::logic
    B1["Slack<br/>Already sequenced"]:::slack
    C["Supabase<br/>Insert call_logs<br/>status = called_no_answer"]:::db
    D["HTTP Request<br/>HeyReach<br/>no-answer campaign"]:::http
    E{"IF<br/>Email valid?"}:::logic
    F["HTTP Request<br/>Instantly<br/>email campaign"]:::http
    G["Supabase<br/>Log email skipped"]:::db
    H["Merge<br/>wait for both"]:::util
    I["Supabase<br/>Insert outreach_events<br/>status = sequenced"]:::db
    J["HubSpot<br/>Log call: No answer"]:::hub
    K["Slack<br/>Update card: enrolled,<br/>finding more people"]:::slack
    L[["Sub-workflow<br/>Start expansion"]]:::util

    A --> B
    B -->|true| B1
    B -->|false| C
    C --> D --> H
    C --> E
    E -->|true| F --> H
    E -->|false| G --> H
    H --> I --> J --> K --> L
```

### 4b. Wrong person

```mermaid
flowchart LR
    classDef db fill:#3ECF8E,color:#000,stroke:#2DA36F
    classDef slack fill:#4A154B,color:#fff,stroke:#4A154B
    classDef util fill:#6B7280,color:#fff,stroke:#4B5563

    A["Supabase<br/>Insert call_logs<br/>status = disqualified"]:::db
    B["Slack<br/>Update card"]:::slack
    C[["Sub-workflow<br/>Start expansion"]]:::util
    A --> B --> C
```

### The "Start expansion" sub-workflow

Used by both 4a and 4b.

```mermaid
flowchart LR
    classDef logic fill:#2E7D5B,color:#fff,stroke:#1F5E43
    classDef db fill:#3ECF8E,color:#000,stroke:#2DA36F
    classDef slack fill:#4A154B,color:#fff,stroke:#4A154B
    classDef http fill:#2D6CDF,color:#fff,stroke:#1F4FA8
    classDef util fill:#6B7280,color:#fff,stroke:#4B5563

    S(["Execute Workflow Trigger<br/>lead_id, company"]):::util
    A["Supabase<br/>Find expansion_runs<br/>same domain, last 30 days"]:::db
    B{"IF<br/>Recent run?"}:::logic
    B1["Slack<br/>Already searched,<br/>link to that thread"]:::slack
    C["Supabase<br/>Insert expansion_runs<br/>status = searching"]:::db
    D["HTTP Request<br/>POST Clay Table 2 webhook"]:::http

    S --> A --> B
    B -->|true| B1
    B -->|false| C --> D
```

### 4c. Picked up

Two separate Slack events: the button click opens the modal, then the modal submit does the work.

```mermaid
flowchart LR
    classDef logic fill:#2E7D5B,color:#fff,stroke:#1F5E43
    classDef db fill:#3ECF8E,color:#000,stroke:#2DA36F
    classDef slack fill:#4A154B,color:#fff,stroke:#4A154B
    classDef hub fill:#FF7A59,color:#fff,stroke:#E5603F
    classDef ai fill:#6B7280,color:#fff,stroke:#4B5563
    classDef evt fill:#fff,color:#111,stroke:#111,stroke-dasharray:4 3

    E1["call_connected"]:::evt --> A["Slack<br/>views.open<br/>call-notes modal"]:::slack
    A -.->|"SDR cancels:<br/>nothing logged"| Z["End"]:::evt

    E2["call_notes_submit"]:::evt --> B["Supabase<br/>Insert call_logs<br/>status = called_connected"]:::db
    B --> C["HubSpot<br/>Log call with notes"]:::hub
    C --> D{"IF<br/>Not interested?"}:::logic
    D -->|true| D1["Slack<br/>Update card: closed out"]:::slack
    D -->|false| F["AI Agent<br/>Draft LinkedIn message<br/>from notes + goal"]:::ai
    F --> G["Slack<br/>Post draft + 4 buttons"]:::slack
    G --> H["Supabase<br/>status = message_drafted"]:::db
```

### 4d. Draft buttons

```mermaid
flowchart LR
    classDef logic fill:#2E7D5B,color:#fff,stroke:#1F5E43
    classDef db fill:#3ECF8E,color:#000,stroke:#2DA36F
    classDef slack fill:#4A154B,color:#fff,stroke:#4A154B
    classDef hub fill:#FF7A59,color:#fff,stroke:#E5603F
    classDef http fill:#2D6CDF,color:#fff,stroke:#1F4FA8
    classDef ai fill:#6B7280,color:#fff,stroke:#4B5563

    S{"Switch<br/>which button?"}:::logic

    S -->|send_message| A1["HTTP Request<br/>HeyReach post-call campaign<br/>custom_message = text"]:::http
    A1 --> A2["Supabase<br/>status = message_sent"]:::db
    A2 --> A3["HubSpot<br/>Note with exact text"]:::hub
    A3 --> A4["Slack<br/>Update card: sent"]:::slack

    S -->|edit_message| B1["Slack<br/>Edit modal with draft"]:::slack
    B1 --> B2["Slack<br/>Replace draft in thread"]:::slack

    S -->|regenerate_message| C1["AI Agent<br/>New, different draft"]:::ai
    C1 --> C2["Slack<br/>Replace draft in thread"]:::slack

    S -->|copy| D1["Slack<br/>Show text in code block"]:::slack
    D1 --> D2["Supabase<br/>message_sent, action = manual"]:::db
```

### 4e. Expansion buttons

```mermaid
flowchart LR
    classDef logic fill:#2E7D5B,color:#fff,stroke:#1F5E43
    classDef db fill:#3ECF8E,color:#000,stroke:#2DA36F
    classDef slack fill:#4A154B,color:#fff,stroke:#4A154B
    classDef util fill:#6B7280,color:#fff,stroke:#4B5563

    S{"Switch<br/>which button?"}:::logic
    S -->|add_suggested_lead| A1["Supabase<br/>status = received"]:::db
    A1 --> A2[["Sub-workflow<br/>Send to Clay Table 1"]]:::util
    S -->|skip_suggested_lead| B1["Supabase<br/>status = skipped"]:::db
    B1 --> B2["Slack<br/>Grey out on card"]:::slack
```

After *Add as lead*, the person goes through Clay Table 1 → WF2 like any other lead, and gets their own lead card in the same thread.

---

## 5. Clay Table 2: Account expansion

Also a Clay table, read as columns.

```mermaid
flowchart LR
    classDef clay fill:#F5C542,color:#000,stroke:#C9A227
    classDef http fill:#2D6CDF,color:#fff,stroke:#1F4FA8

    A["Webhook source<br/>run_id, company,<br/>original person"]:::clay
    B["Find people at company<br/>buyer persona filter<br/>max 8"]:::clay
    C["Formula<br/>expected_total"]:::clay
    D["HTTP API column<br/>POST count to WF5"]:::http
    E["Child table, per person:<br/>drop original person"]:::clay
    F["Enrich person<br/>+ email waterfall<br/>no phone"]:::clay
    G["AI column<br/>fit score 1-5 + reason"]:::clay
    H["HTTP API column<br/>POST person to WF5"]:::http

    A --> B --> C --> D
    B --> E --> F --> G --> H
```

---

## 6. WF5 Expansion results

**Trigger:** Clay Table 2 posts either the count or one person.

```mermaid
flowchart LR
    classDef trigger fill:#FF6D5A,color:#fff,stroke:#E5533F
    classDef logic fill:#2E7D5B,color:#fff,stroke:#1F5E43
    classDef db fill:#3ECF8E,color:#000,stroke:#2DA36F
    classDef slack fill:#4A154B,color:#fff,stroke:#4A154B
    classDef util fill:#6B7280,color:#fff,stroke:#4B5563

    A(["Webhook<br/>POST /sdr-expansion"]):::trigger
    B["Respond to Webhook<br/>200 OK"]:::util
    C{"Switch<br/>message type"}:::logic

    D["Supabase<br/>Save expected_total"]:::db
    E{"IF<br/>Total = 0?"}:::logic
    E1["Slack<br/>No other matching people<br/>run = empty"]:::slack
    E2["Wait for people"]:::util

    F["Supabase<br/>Find lead by URL"]:::db
    G{"IF<br/>Already in Supabase?"}:::logic
    H["Supabase<br/>Insert lead<br/>status = suggested"]:::db
    J["Supabase<br/>received_count + 1"]:::db
    K{"IF<br/>received = expected?"}:::logic
    L["Supabase<br/>Get suggested leads,<br/>sort by fit"]:::db
    M["Slack<br/>Post expansion card<br/>Add / Skip per person"]:::slack
    N["Supabase<br/>run = posted"]:::db
    K0["Wait for more"]:::util

    A --> B --> C
    C -->|count| D --> E
    E -->|true| E1
    E -->|false| E2
    C -->|person| F --> G
    G -->|false| H --> J
    G -->|true| J
    J --> K
    K -->|true| L --> M --> N
    K -->|false| K0
```

---

## 7. WF4 Errors and sweeps

Two triggers, running alongside everything.

```mermaid
flowchart LR
    classDef trigger fill:#FF6D5A,color:#fff,stroke:#E5533F
    classDef db fill:#3ECF8E,color:#000,stroke:#2DA36F
    classDef slack fill:#4A154B,color:#fff,stroke:#4A154B

    A(["Error Trigger<br/>any of WF1, 2, 3, 5 fails"]):::trigger
    A1["Supabase<br/>Insert workflow_errors"]:::db
    A2["Supabase<br/>Lead status = error"]:::db
    A3["Slack<br/>Something failed at step X<br/>+ Retry button"]:::slack
    A --> A1 --> A2 --> A3

    B(["Schedule Trigger<br/>every 10 min"]):::trigger
    B1["Supabase<br/>Leads stuck in enriching<br/>over 15 min"]:::db
    B2["Slack<br/>Alert the SDR"]:::slack
    B3["Supabase<br/>Runs stuck in searching<br/>over 10 min"]:::db
    B4["Slack<br/>Post partial expansion card"]:::slack
    B --> B1 --> B2
    B --> B3 --> B4
```
