#!/usr/bin/env bash
set -e

echo "==> Clean in case canton was changed..."
mix clean

echo "==> Fetching dependencies..."
mix deps.get

echo "==> Running migrations..."
mix ecto.migrate

echo "==> Starting Phoenix server (with code reloading + asset watchers)..."
# Named node so a remote console can attach to the *running* server, e.g.
#   docker compose exec elixir iex --sname console --remsh elixir-ebau@$(hostname)
exec elixir --sname elixir-ebau -S mix phx.server
