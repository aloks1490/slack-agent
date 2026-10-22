<!--
Prompt for clients/llm.py -> research(). Turns enrichment data into a short brief
for a cold call. Output is parsed into the Research model (structured output).
Placeholders in {curly_braces} are filled in by the code. Phase 2.
Starting point from the project doc; tune it after reading real outputs.
-->

You are helping an SDR prepare a cold call.

Person: {full_name}, {title} at {company_name} ({company_size}, {industry}).
About: {about}
Recent activity: {recent_posts}
Company: {company_description}

Return:
- summary: 3 short bullets on who they are and what they likely care about
- talking_points: 3 specific openers grounded ONLY in the data above
- icp_fit: yes or no, from seniority and company size

No guesses. If data is missing, say so.
