#!/bin/bash
source ./config.sh

echo "---------------------------"
echo "eCH0211 - POST inquiry"
echo "---------------------------"

ebau_nr="2024-1"
dossier_id="5"
service_id="19"

for i in "${!ech0211_credentials[@]}"
do
xml_payload=$(cat <<EOF
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>

<ns16:delivery xmlns:ns2="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns4="http://www.ech.ch/xmlns/eCH-0010/6" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0129/5" xmlns:ns6="http://www.ech.ch/xmlns/eCH-0044/4" xmlns:ns5="http://www.ech.ch/xmlns/eCH-0007/6" xmlns:ns8="http://www.ech.ch/xmlns/eCH-0008/3" xmlns:ns7="http://www.ech.ch/xmlns/eCH-0097/2" xmlns:ns13="http://www.ech.ch/xmlns/eCH-0046/1" xmlns:ns9="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:ns12="http://www.ech.ch/xmlns/eCH-0044/1" xmlns:ns11="http://www.ech.ch/xmlns/eCH-0147/T0/1" xmlns:ns10="http://www.ech.ch/xmlns/eCH-0039/2" xmlns:ns16="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns15="http://www.ech.ch/xmlns/eCH-0058/3" xmlns:ns14="http://www.ech.ch/xmlns/eCH-0010/3">
<ns2:deliveryHeader>
<ns9:senderId>gemdat://test-123</ns9:senderId>
<ns9:messageId>ignored</ns9:messageId>
<ns9:messageType>ignored</ns9:messageType>
<ns9:sendingApplication>
<ns9:manufacturer>GemDat Informatik AG</ns9:manufacturer>
<ns9:product>eBaugesucheZH</ns9:product>
<ns9:productVersion>1.2.0</ns9:productVersion>
</ns9:sendingApplication>
<ns9:subject>Bauprojekttitel</ns9:subject>
<!-- wird ignoriert -->
<ns9:messageDate>2019-11-11T00:00:00.000Z</ns9:messageDate>
<ns9:action>1</ns9:action>
<ns9:testDeliveryFlag>true</ns9:testDeliveryFlag>
</ns2:deliveryHeader>
<ns2:eventRequest>
<ns2:eventType>task</ns2:eventType>
<!-- wird ignoriert -->
<ns2:planningPermissionApplicationIdentification>
<ns2:localID>
<ns3:IdCategory>eBauNr</ns3:IdCategory>
<ns3:Id>${ebau_nr}</ns3:Id>
</ns2:localID>
<ns2:otherID>
<ns3:IdCategory>eBauNr</ns3:IdCategory>
<!-- wird ignoriert -->
<ns3:Id>${ebau_nr}</ns3:Id>
<!-- wird ignoriert -->
</ns2:otherID>
<ns2:dossierIdentification>${dossier_id}</ns2:dossierIdentification>
</ns2:planningPermissionApplicationIdentification>
<ns2:directive>
<uuid>00000000-0000-0000-0000-000000000000</uuid>
<!-- wird ignoriert -->
<instruction>process</instruction>
<!-- wird ignoriert -->
<priority>undefined</priority>
<!-- wird ignoriert -->
<deadline>2020-03-15</deadline>
<comments>
<ns10:comment>Anforderung einer Stellungnahme</ns10:comment>
<!-- wird ignoriert -->
</comments>
</ns2:directive>
<ns2:extension>
<!-- ID der eingeladenen Organisation. -->
<serviceId>${service_id}</serviceId>
</ns2:extension>
</ns2:eventRequest>
</ns16:delivery>
EOF
)
	ech0211_login "$i" "${ech0211_credentials[$i]}"
	echo " > perform request[inquiry] for client_id: $i"
	echo -e "\n---------------------------"
	curl -X POST 'http://ember-ebau.localhost/ech/v1/send/' \
	-H "Authorization: Bearer $token" \
	-H 'accept: application/xml' \
	-H "x-camac-group: ${camac_group_id}" \
	-H 'Content-Type: application/xml' \
	-d "$xml_payload"
	echo -e "\n---------------------------"
done

