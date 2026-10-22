"""Entry point: `uv run sdr-agent` starts the bot.

Planned:
- main()
    1. Load settings (config.get_settings) and set up logging.
    2. Build the Slack app with all listeners (slack.app.create_app).
    3. Start the scheduler (jobs.scheduled.start) for sweeps and reports.
    4. Start Slack Socket Mode (slack_bolt.adapter.socket_mode.SocketModeHandler)
       and block until stopped.

Phase: 0 (hello world: reply "pong" in a thread)
"""
