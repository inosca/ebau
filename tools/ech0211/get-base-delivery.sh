#!/bin/bash
source ./config.sh

echo "---------------------------"
echo "eCH0211 - GET base delivery"
echo "---------------------------"

dossier_id="5"

for i in "${!ech0211_credentials[@]}"
do
	ech0211_login "$i" "${ech0211_credentials[$i]}"
	echo " > perform request[base delivery] for client_id: $i"
	echo -e "\n---------------------------"
	curl -X GET "${ech0211_endpoint}/ech/v1/application/${dossier_id}" \
	-H "Authorization: Bearer $token" \
	-H 'accept: application/xml' \
	-H "x-camac-group: ${camac_group_id}" \
	-H 'Content-Type: application/xml'
	echo -e "\n---------------------------"
done
