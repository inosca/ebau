#!/usr/bin/env python3

from utils import each_client, endpoint, print_response, print_title

document_uuid = "c11b2559-aeb8-43f6-a73f-37cca84f9e9e"

print_title("eCH0211 - DELETE document void")

for session, client_id in each_client():
    print(f" > perform request[delete document void] for client_id: {client_id}")

    response = session.delete(
        f"{endpoint}/ech/v1/documents/{document_uuid}/void",
        headers={"accept": "application/vnd.api+json"},
    )

    print_response(response)
