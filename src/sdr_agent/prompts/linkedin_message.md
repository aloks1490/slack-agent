<!--
Prompt for clients/llm.py -> draft_message(). Writes the follow-up LinkedIn message
after a connected call. Output is parsed into the LinkedInDraft model. Phase 6.
Starting point from the project doc.
-->

Write a LinkedIn message from {sdr_name} to {first_name}, {title} at {company_name}.
They just spoke on the phone.

Call notes: {call_notes}
Goal of this message: {message_goal}

Rules:
- Under 300 characters, so it also fits a connection-request note
- Reference one specific thing they said on the call
- One clear next step, no hard pitch
- Plain, human tone; no emojis, no "I hope this finds you well"
- Never invent facts that are not in the notes
