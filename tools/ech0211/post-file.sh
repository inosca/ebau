#!/bin/bash
source ./config.sh

echo "---------------------------"
echo "eCH0211 - POST file"
echo "---------------------------"

dossier_id="12"
file_link="${ech0211_endpoint}/ech/v1/files"

for i in "${!ech0211_credentials[@]}"
do
	ech0211_login "$i" "${ech0211_credentials[$i]}"
	echo " > perform request[post file] for client_id: $i"
	echo -e "\n---------------------------"
	curl -D - -X POST ${file_link} \
	-H "Authorization: Bearer $token" \
	-H 'accept: application/json' \
	-H "x-camac-group: ${camac_group_id}" \
	-H 'Content-Type: multipart/form-data' \
	-F "content=@./test.jpg;type=image/jpeg" \
	-F "instance=${dossier_id}" \
	-F "category=beilagen-zum-gesuch"
	echo -e "\n---------------------------"
done
