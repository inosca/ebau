#!/bin/bash

# A script to perform a token exchange and then call the eeba_export API.
#
# Usage: ./export.sh <dossier_id> <subject_token>

set -euo pipefail

# Load secrets from .env file
if [ ! -f ".env" ]; then
    echo "Error: .env file not found." >&2
    exit 1
fi
source .env

if [ -z "${CLIENT_SECRET-}" ] || [ -z "${API_SECRET-}" ]; then
    echo "Error: CLIENT_SECRET and API_SECRET must be set in the .env file." >&2
    exit 1
fi

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <dossier_id> <subject_token>" >&2
    exit 1
fi

DOSSIER_ID="$1"
SUBJECT_TOKEN="$2"

TOKEN_ENDPOINT="https://test.ebau.gr.ch/auth/realms/ebau/protocol/openid-connect/token"
API_ENDPOINT="https://test.ebau.gr.ch/api/v1/instances/${DOSSIER_ID}/eeba_export"
CLIENT_ID="eeba-token-exchange"

EXCHANGED_TOKEN=$(curl -s -X POST "${TOKEN_ENDPOINT}" \
    -u "${CLIENT_ID}:${CLIENT_SECRET}" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "grant_type=urn:ietf:params:oauth:grant-type:token-exchange" \
    -d "subject_token=${SUBJECT_TOKEN}" \
    -d "subject_token_type=urn:ietf:params:oauth:token-type:access_token" \
    -d "requested_token_type=urn:ietf:params:oauth:token-type:access_token" \
    -d "scope=eeba-export openid" | jq -r '.access_token')

if [ -z "$EXCHANGED_TOKEN" ] || [ "$EXCHANGED_TOKEN" == "null" ]; then
    echo "Error: Failed to retrieve exchanged token." >&2
    exit 1
fi

curl --location "${API_ENDPOINT}" \
    --header "X-EBAU-EEBA-SECRET: ${API_SECRET}" \
    --header "Authorization: Bearer ${EXCHANGED_TOKEN}" | jq .
