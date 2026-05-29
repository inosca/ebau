#!/bin/sh
set -eu

# Required environment variables:
[ -n "${GARAGE_ACCESS_KEY_ID:-}" ] || { echo "Missing GARAGE_ACCESS_KEY_ID"; exit 1; }
[ -n "${GARAGE_SECRET_KEY:-}" ]    || { echo "Missing GARAGE_SECRET_KEY"; exit 1; }
[ -n "${GARAGE_KEY_NAME:-}" ]      || { echo "Missing GARAGE_KEY_NAME"; exit 1; }

ACCESS_KEY_ID="$GARAGE_ACCESS_KEY_ID"
SECRET_KEY="$GARAGE_SECRET_KEY"
KEY_NAME="$GARAGE_KEY_NAME"

# Optional environment variables:
CLUSTER_NAME=${GARAGE_CLUSTER_NAME:-dev}
CLUSTER_CAPACITY=${GARAGE_CLUSTER_CAPACITY:-10GiB}

garage server &
SERVER_PID=$!

echo "Waiting for Garage server to respond..."
until garage status >/dev/null 2>&1; do
    sleep 1
done
echo "Garage $(garage --version) is online."

RAW_NODE_ID="$(garage node id | tr -d '\r\n')"
NODE_ID=${RAW_NODE_ID%%@*}

bootstrap()
{
	echo "Applying layout for node '$NODE_ID'..."
	garage layout assign -z "$CLUSTER_NAME" -c "$CLUSTER_CAPACITY" "$NODE_ID" || true
	garage layout apply --version 1 || true

	echo "Importing known key..."
	garage key import --yes -n "$KEY_NAME" "$ACCESS_KEY_ID" "$SECRET_KEY"

	echo "Creating buckets and setting permissions..."
	for bucket in dms-media alexandria-media ebau-media; do
		garage bucket create "$bucket" || true
		garage bucket allow --read --write --owner "$bucket" --key "$KEY_NAME" || true
	done
}

if garage key list | awk 'NR>1 {print $3}' | grep -qx "$KEY_NAME"; then
	echo "Key '$KEY_NAME' already exists. Skipping bootstrap."
else
	echo "Bootstrap starting (key '$KEY_NAME' does not exist)."
	bootstrap
	echo "Bootstrap complete."
fi

echo "Node: $NODE_ID"
wait "$SERVER_PID"
