#!/usr/bin/env python3

from utils import (
    each_client,
    endpoint,
    print_delimiter,
    print_response,
    print_title,
)

print_title("eCH0211 - GET me")

for session, client_id in each_client():
    print(f" > perform request[me] for client_id: {client_id}")

    response = session.get(
        f"{endpoint}/api/v1/me",
        headers={"accept": "application/vnd.api+json"},
    )

    print_response(response)

    result = response.json()
    user_id = result["data"]["id"]
    group_ids = [rel["id"] for rel in result["data"]["relationships"]["groups"]["data"]]

    print(f"User ID: {user_id}")
    print(f"Group IDs: {', '.join(group_ids)}")
    print_delimiter()
