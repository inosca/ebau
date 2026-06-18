#!/usr/bin/env python3

import sys
from xml.etree import ElementTree

from utils import each_client, endpoint, print_response, print_title

last_message_id = sys.argv[1] if len(sys.argv) > 1 else None

if last_message_id:
    print(f"Using provided last_message_id: {last_message_id}")
else:
    print("Reading the first message")

print_title("eCH0211 - GET message")

for session, client_id in each_client():
    print(f" > perform request[message] for client_id: {client_id}")

    response = session.get(
        f"{endpoint}/ech/v1/message/",
        params={"last": last_message_id} if last_message_id else None,
        headers={"accept": "application/xml"},
    )

    print_response(response)

    message_id = None
    message_type = None

    if response.text:
        try:
            root = ElementTree.fromstring(response.text)
            namespace = "{http://www.ech.ch/xmlns/eCH-0058/5}"
            message_id = root.findtext(f".//{namespace}messageId")
            message_type = root.findtext(f".//{namespace}messageType")
        except ElementTree.ParseError:
            print("Warning: XML parsing failed.")

    print("Extracted Information:")
    print(f"Message ID: {message_id or 'Not found'}")
    print(f"Message Type: {message_type or 'Not found'}")
