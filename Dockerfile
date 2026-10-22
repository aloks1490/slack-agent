# Container image for running the bot 24/7 (Phase 7: deploy to Railway or Fly.io).
#
# Plan:
# - Start from a slim Python 3.12 image and install uv.
# - Copy pyproject.toml + uv.lock first, run `uv sync --frozen --no-dev`
#   (cached layer), then copy src/.
# - Run as a non-root user.
# - CMD: `uv run sdr-agent`
#
# Notes:
# - No EXPOSE needed: Socket Mode connects out to Slack.
# - Secrets come from the host's environment variables, never baked into the image.
# - Run exactly ONE instance (Socket Mode + in-process job runner).
