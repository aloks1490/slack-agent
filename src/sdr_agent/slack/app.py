"""Builds the Slack Bolt app and registers every listener.

Planned:
- create_app(settings) -> slack_bolt.App
    events:  app_mention                              -> handlers.mentions
    actions: call_connected, call_no_answer, wrong_person, open_linkedin
                                                      -> handlers.call_buttons
             send_message, edit_message, regenerate_message, copy_message
                                                      -> handlers.modals
             add_suggested_lead, skip_suggested_lead  -> handlers.expansion_buttons
             retry_step                               -> handlers.retry
    views:   call_notes_submit, edit_message_submit   -> handlers.modals

Socket Mode: started from main.py with the app-level token (SLACK_APP_TOKEN).

Phase: 0
"""
