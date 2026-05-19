#!/bin/bash
source ./config.sh

echo "---------------------------"
echo "eCH0211 - PATCH document"
echo "---------------------------"

document_id="d9661ff6-d91a-44cd-b20e-d0ec80933aa3"
document_link="${ech0211_endpoint}/ech/v1/documents/${document_id}"

for i in "${!ech0211_credentials[@]}"
do
	ech0211_login "$i" "${ech0211_credentials[$i]}"
	echo " > perform request[patch document] for client_id: $i"
	echo -e "\n---------------------------"
	curl -D - -X PATCH "${document_link}" \
	-H "Authorization: Bearer $token" \
	-H 'content-type: application/vnd.api+json' \
	-H "x-camac-group: ${camac_group_id}" \
	--data @- <<EOF
{
  "data": {
    "type": "ech0211-documents",
    "id": "${document_id}",
    "attributes": {
      "title": "test-1.jpg",
      "description": "Updated document description",
      "date": "2024-06-01"
    },
    "relationships": {
      "category": {
        "data": {
          "type": "ech0211-document-categories",
          "id": "alle-beteiligten"
        }
      }
    }
  }
}
EOF
	echo -e "\n---------------------------"
done
