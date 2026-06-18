#!/usr/bin/env python3

from utils import each_client, endpoint, print_response, print_title

instance_id = 12
category_id = "beilagen-zum-gesuch"
file_path = "test.pdf"

print_title("eCH0211 - POST file")

for session, client_id in each_client():
    print(f" > perform request[post file] for client_id: {client_id}")

    with open(file_path, "rb") as file:
        response = session.post(
            f"{endpoint}/ech/v1/files",
            data={
                "instance": instance_id,
                "category": category_id,
            },
            files={
                "content": (file_path, file, "application/pdf"),
            },
            headers={"accept": "application/json"},
        )

    print_response(response)
