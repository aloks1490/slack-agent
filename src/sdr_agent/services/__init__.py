"""Services: the business logic. Each function is one step of a flow.

Rules: never import Slack code; talk to the outside world only through clients;
check the lead's status before acting and set it after.
"""
