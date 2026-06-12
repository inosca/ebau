#!/usr/bin/env python3

from utils import each_client, endpoint, paginate, print_response, print_title

instance_id = 12

print_title("eCH0211 - GET documents")

for session, client_id in each_client():
    print(f" > perform request[get documents] for client_id: {client_id}")

    response = paginate(session).get(
        f"{endpoint}/ech/v1/documents",
        params={"instance": instance_id},
        headers={"accept": "application/vnd.api+json"},
    )

    print_response(response)
