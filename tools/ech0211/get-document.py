#!/usr/bin/env python3

from utils import each_client, endpoint, print_response, print_title

document_id = "4c094968-dddf-4534-b75c-2605261efe40"

print_title("eCH0211 - GET document")

for session, client_id in each_client():
    print(f" > perform request[get document] for client_id: {client_id}")

    response = session.get(
        f"{endpoint}/ech/v1/documents/{document_id}",
        headers={"accept": "application/vnd.api+json"},
    )

    print_response(response)
