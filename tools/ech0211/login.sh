#!/bin/bash
source ./config.sh

echo "---------------------------"
echo "eCH0211 - GET /api/v1/me"
echo "---------------------------"

for i in "${!ech0211_credentials[@]}"
do
	ech0211_login "$i" "${ech0211_credentials[$i]}"
	echo " > perform request[me] for client_id: $i"
	echo -e "\n---------------------------"
	user_info=$(curl -X GET "${ech0211_endpoint}/api/v1/me" -H "Authorization: Bearer $token")
	echo "$user_info" | jq '.'
	echo "id: $(echo "$user_info" | jq -r '.data.id')"
	echo "groups: $(echo "$user_info" | jq -r '[.data.relationships.groups.data[].id] | join(", ")')"
	echo -e "\n---------------------------"
done
