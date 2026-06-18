#!/usr/bin/env python3

from utils import each_client, endpoint, print_response, print_title

file_uuid = "0a41a9f1-31cb-4839-9a54-2052401cf9af"

print_title("eCH0211 - DELETE file")

for session, client_id in each_client():
    print(f" > perform request[delete file] for client_id: {client_id}")

    response = session.delete(
        f"{endpoint}/ech/v1/files/{file_uuid}",
        headers={"accept": "application/json"},
    )

    print_response(response)
