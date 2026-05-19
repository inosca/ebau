#!/bin/bash
set -e

echo "==> Installing dependencies..."
mix deps.get

echo "==> Compiling dependencies (this takes a few minutes on first run)..."
mix deps.compile

echo "==> Compiling application..."
mix compile

echo "==> Running migrations..."
mix ecto.migrate

echo "==> Starting Phoenix server..."
elixir --sname elixir-ebau -S mix phx.server
