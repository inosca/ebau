#!/bin/sh
set -eu

CONFIG=/etc/garage.toml
GARAGE="/garage -c $CONFIG"

[ -n "${GARAGE_ACCESS_KEY_ID:-}" ] || { echo "Missing GARAGE_ACCESS_KEY_ID"; exit 1; }
[ -n "${GARAGE_SECRET_KEY:-}" ]   || { echo "Missing GARAGE_SECRET_KEY"; exit 1; }
[ -n "${GARAGE_KEY_NAME:-}" ]      || { echo "Missing GARAGE_KEY_NAME"; exit 1; }

ACCESS_KEY_ID="$GARAGE_ACCESS_KEY_ID"
SECRET_KEY="$GARAGE_SECRET_KEY"
KEY_NAME="$GARAGE_KEY_NAME"

$GARAGE server &
SERVER_PID=$!

echo "Waiting for Garage server to respond..."
until $GARAGE status >/dev/null 2>&1; do
    sleep 1
done
echo "Garage $($GARAGE --version) is online."

RAW_NODE_ID="$($GARAGE node id | tr -d '\r\n')"
NODE_ID="$(printf '%s' "$RAW_NODE_ID" | sed 's/@.*$//')"

if $GARAGE key list | awk 'NR>1 {print $3}' | grep -qx "$KEY_NAME"; then
    echo "Key '$KEY_NAME' already exists. Skipping bootstrap."
    echo "Node: $NODE_ID"
    wait "$SERVER_PID"
    exit 0
fi

echo "Bootstrap starting (key '$KEY_NAME' does not exist)."

echo "Applying layout for node '$NODE_ID'..."
$GARAGE layout assign -z dev -c 10G "$NODE_ID" || true
$GARAGE layout apply --version 1 || true

echo "Importing known key..."
$GARAGE key import --yes -n "$KEY_NAME" "$ACCESS_KEY_ID" "$SECRET_KEY"

echo "Creating buckets and setting permissions..."
$GARAGE bucket create dms-media || true
$GARAGE bucket allow --read --write --owner dms-media --key "$KEY_NAME" || true
$GARAGE bucket create alexandria-media || true
$GARAGE bucket allow --read --write --owner alexandria-media --key "$KEY_NAME" || true
$GARAGE bucket create ebau-media || true
$GARAGE bucket allow --read --write --owner ebau-media --key "$KEY_NAME" || true

echo "Bootstrap complete."
echo "Node: $NODE_ID"
wait "$SERVER_PID"
