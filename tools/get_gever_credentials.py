#!/usr/bin/python3

import subprocess
import json
import sys

target = "gever-dev-env"
secret = "ag01-u02"

if len(sys.argv) == 3:
    target, secret = sys.argv[1:]

elif len(sys.argv) == 2:
    secret = sys.argv[1]

elif len(sys.argv) == 1:
    print(f"Using default target and secret: {target}, {secret}")
    print("If you want to override the secret, pass it as commandline.")
    print("If you want to override the target and secret, pass both as commandline.")
    print("")
    print("Examples:")
    print(
        f"  {sys.argv[0]}      # (current call): use target {target}, secret {secret}"
    )
    print(f"  {sys.argv[0]} <secret>   # use <secret> instead of {secret}")
    print(
        f"  {sys.argv[0]} <target> <secret>  use <target> and <secret> instead of {target} and {secret}"
    )
    print("")

output = subprocess.check_output(
    [
        "vault",
        "kv",
        "get",
        "-address",
        "https://vault.adfinis.com",
        "-format=json",
        f"kantonbern-kv/partner/cmiag/{target}/{secret}",
    ]
)

print("Write the following lines to your `.env` file:")
for key in ["client_id", "client_secret", "token_url", "api_base_url"]:
    env_var = f"gever_{key}".upper()
    value = json.loads(output)["data"]["data"][key]
    print(f"{env_var}={value}")
