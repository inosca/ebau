#!/usr/bin/env python3

from utils import each_client, endpoint, print_response, print_title

instance_id = 12

print_title("eCH0211 - GET base delivery")

for session, client_id in each_client():
    print(f" > perform request[base delivery] for client_id: {client_id}")

    response = session.get(
        f"{endpoint}/ech/v1/application/{instance_id}",
        headers={"accept": "application/xml"},
    )

    print_response(response)
