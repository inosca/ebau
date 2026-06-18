#!/usr/bin/env python3

from utils import each_client, endpoint, print_response, print_title

instance_id = 12
special_id = "2026-1"
source_organisation_id = 18
target_organisation_id = 19

xml_payload = f"""<?xml version="1.0" ?>
<ns1:delivery xmlns:ns1="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0129/5" xmlns:ns4="http://www.ech.ch/xmlns/eCH-0097/2" xmlns:ns5="http://www.ech.ch/xmlns/eCH-0007/6" xmlns:ns6="http://www.ech.ch/xmlns/eCH-0010/6">
    <ns1:deliveryHeader>
        <ns2:senderId>gemdat://test-123</ns2:senderId>
        <ns2:messageId>ignored</ns2:messageId>
        <ns2:messageType>ignored</ns2:messageType>
        <ns2:sendingApplication>
            <ns2:manufacturer>GemDat Informatik AG</ns2:manufacturer>
            <ns2:product>eBaugesucheZH</ns2:product>
            <ns2:productVersion>1.1.1</ns2:productVersion>
        </ns2:sendingApplication>
        <ns2:subject>change responsibility</ns2:subject>
        <ns2:messageDate>2019-11-07T07:45:04.292204Z</ns2:messageDate>
        <ns2:action>1</ns2:action>
        <ns2:testDeliveryFlag>true</ns2:testDeliveryFlag>
    </ns1:deliveryHeader>
    <ns1:eventChangeResponsibility>
        <ns1:eventType>change responsibility</ns1:eventType><!-- wird ignoriert -->
        <ns1:planningPermissionApplicationIdentification>
            <ns1:localID>
                <ns3:IdCategory>eBauNr</ns3:IdCategory>
                <ns3:Id>{special_id}</ns3:Id>
            </ns1:localID>
            <ns1:otherID>
                <ns3:IdCategory>instanceID</ns3:IdCategory>
                <ns3:Id>unknown</ns3:Id>
            </ns1:otherID>
            <ns1:dossierIdentification>{instance_id}</ns1:dossierIdentification>
        </ns1:planningPermissionApplicationIdentification>
        <ns1:entryOffice>
            <ns1:entryOfficeIdentification><!-- wird ignoriert, da in eBau bereits bekannt -->
                <ns4:uid>
                    <ns4:uidOrganisationIdCategorie>CHE</ns4:uidOrganisationIdCategorie>
                    <ns4:uidOrganisationId>123</ns4:uidOrganisationId>
                </ns4:uid>
                <ns4:localOrganisationId>
                    <ns4:organisationIdCategory>ebaube</ns4:organisationIdCategory>
                    <ns4:organisationId>{source_organisation_id}</ns4:organisationId>
                </ns4:localOrganisationId>
                <ns4:organisationName>Leitbeh&#xF6;rde Testgemeinde</ns4:organisationName>
                <ns4:legalForm>0223</ns4:legalForm>
            </ns1:entryOfficeIdentification>
            <ns1:municipality>
                <ns5:municipalityName>Testgemeinde</ns5:municipalityName>
                <ns5:cantonAbbreviation>GR</ns5:cantonAbbreviation>
            </ns1:municipality>
        </ns1:entryOffice>
        <ns1:responsibleDecisionAuthority>
            <ns1:decisionAuthority>
                <ns3:buildingAuthorityIdentificationType>
                    <ns4:uid>
                        <ns4:uidOrganisationIdCategorie>CHE</ns4:uidOrganisationIdCategorie>
                        <ns4:uidOrganisationId>123</ns4:uidOrganisationId>
                    </ns4:uid>
                    <ns4:localOrganisationId>
                        <ns4:organisationIdCategory>ebaube</ns4:organisationIdCategory>
                        <!-- ID der neuen Leitbehörde -->
                        <ns4:organisationId>{target_organisation_id}</ns4:organisationId>
                    </ns4:localOrganisationId>
                    <ns4:organisationName>Leitbehörde Madiswil</ns4:organisationName>
                    <ns4:legalForm>0223</ns4:legalForm>
                </ns3:buildingAuthorityIdentificationType>
                <ns3:address>
                    <ns6:street>Testweg 5</ns6:street>
                    <ns6:town>Madiswil</ns6:town>
                    <ns6:swissZipCode>3500</ns6:swissZipCode>
                    <ns6:country>
                        <ns6:countryNameShort>CH</ns6:countryNameShort>
                    </ns6:country>
                </ns3:address>
            </ns1:decisionAuthority>
        </ns1:responsibleDecisionAuthority>
    </ns1:eventChangeResponsibility>
</ns1:delivery>
"""

print_title("eCH0211 - POST change responsibility")

for session, client_id in each_client():
    print(f" > perform request[change responsibility] for client_id: {client_id}")

    response = session.post(
        f"{endpoint}/ech/v1/send/",
        data=xml_payload.encode("utf-8"),
        headers={
            "accept": "application/xml",
            "content-type": "application/xml",
        },
    )

    print_response(response)
