#!/usr/bin/env python3

from utils import each_client, endpoint, print_response, print_title

document_uuid = "c11b2559-aeb8-43f6-a73f-37cca84f9e9e"
category_id = "alle-beteiligten"
title = "test-1.pdf"
description = "Test document description"
date = "2024-06-01"

payload = {
    "data": {
        "type": "ech0211-documents",
        "id": document_uuid,
        "attributes": {
            "title": title,
            "description": description,
            "date": date,
        },
        "relationships": {
            "category": {
                "data": {
                    "type": "ech0211-document-categories",
                    "id": category_id,
                }
            }
        },
    }
}

print_title("eCH0211 - PATCH document")

for session, client_id in each_client():
    print(f" > perform request[patch document] for client_id: {client_id}")

    response = session.patch(
        f"{endpoint}/ech/v1/documents/{document_uuid}",
        json=payload,
        headers={
            "accept": "application/vnd.api+json",
            "content-type": "application/vnd.api+json",
        },
    )

    print_response(response)
