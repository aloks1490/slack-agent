-- Slack SDR Agent: Supabase schema
-- Paste this whole file into Supabase > SQL Editor > New query, then click Run.

create table leads (
  id uuid primary key default gen_random_uuid(),
  linkedin_url text unique not null,
  first_name text, last_name text, full_name text,
  title text, headline text, location text,
  company_name text, company_domain text, company_linkedin_url text,
  company_size text, industry text,
  work_email text, email_status text,
  phone text, phone_type text,
  linkedin_followers int, linkedin_connections int,
  research_summary text, talking_points text,
  enrichment jsonb,
  hubspot_contact_id text, hubspot_company_id text,
  sdr_slack_id text, slack_channel_id text, slack_thread_ts text,
  source text not null default 'slack_command',   -- or 'account_expansion'
  parent_lead_id uuid references leads(id),       -- set for suggested colleagues
  fit_reason text,                                -- why Clay suggested this person
  status text not null default 'received',
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create table expansion_runs (
  id uuid primary key default gen_random_uuid(),
  lead_id uuid references leads(id),
  company_domain text,
  expected_total int,
  received_count int default 0,
  slack_message_ts text,
  status text default 'searching',                -- searching, posted, empty, error
  created_at timestamptz default now()
);

create table call_logs (
  id uuid primary key default gen_random_uuid(),
  lead_id uuid references leads(id),
  sdr_slack_id text,
  outcome text check (outcome in ('no_answer','connected','wrong_person','voicemail')),
  notes text,
  created_at timestamptz default now()
);

create table outreach_events (
  id uuid primary key default gen_random_uuid(),
  lead_id uuid references leads(id),
  channel text check (channel in ('linkedin','email')),
  action text,        -- heyreach_enrolled, instantly_enrolled, message_drafted, message_sent
  message text,
  external_id text,   -- campaign or message ID from HeyReach / Instantly
  created_at timestamptz default now()
);

create table workflow_errors (
  id bigserial primary key,
  workflow text, step text,
  lead_id uuid, error text, payload jsonb,
  created_at timestamptz default now()
);

create index on leads (status);
create index on leads (parent_lead_id);
create index on leads (company_domain);
create index on call_logs (lead_id);
create index on outreach_events (lead_id);

-- Keep updated_at current on every change to a lead
create or replace function set_updated_at() returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

create trigger leads_updated_at before update on leads
  for each row execute function set_updated_at();

-- Row Level Security on: only the service-role key (kept in n8n) can read/write
alter table leads enable row level security;
alter table expansion_runs enable row level security;
alter table call_logs enable row level security;
alter table outreach_events enable row level security;
alter table workflow_errors enable row level security;
