#!/bin/sh
set -e

mix deps.get
mix deps.compile

mix phx.server
