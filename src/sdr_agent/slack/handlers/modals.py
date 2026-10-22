"""Connected-call flow in Slack: the call-notes modal, the draft buttons and the edit modal.

Planned:
- on_call_notes_submit(ack, view, body)
    read outcome / notes / goal and the lead id from private_metadata ->
    job: services.messaging.record_connected_call (+ create_draft) -> post draft card
- on_send_message        -> services.messaging.send_via_heyreach, update the card
- on_edit_message        -> open edit modal pre-filled with the draft
- on_edit_message_submit -> replace the draft in the thread
- on_regenerate_message  -> services.messaging.regenerate_draft
- on_copy_message        -> show the text in a code block, mark_sent_manually

Cancelling a modal logs nothing. Phase: 6
"""
