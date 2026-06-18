#!/usr/bin/env python3

from utils import each_client, endpoint, print_response, print_title

document_uuid = "c11b2559-aeb8-43f6-a73f-37cca84f9e9e"

print_title("eCH0211 - POST document decision")

for session, client_id in each_client():
    print(f" > perform request[post document decision] for client_id: {client_id}")

    response = session.post(
        f"{endpoint}/ech/v1/documents/{document_uuid}/decision",
        headers={"accept": "application/vnd.api+json"},
    )

    print_response(response)
