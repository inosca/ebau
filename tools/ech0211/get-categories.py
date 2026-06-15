#!/usr/bin/env python3

from utils import each_client, endpoint, paginate, print_response, print_title

print_title("eCH0211 - GET categories")

for session, client_id in each_client():
    print(f" > perform request[get categories] for client_id: {client_id}")

    response = paginate(session).get(
        f"{endpoint}/ech/v1/categories",
        headers={"accept": "application/vnd.api+json"},
    )

    print_response(response)
