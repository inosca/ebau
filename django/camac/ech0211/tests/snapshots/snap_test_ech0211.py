# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_generate_delivery[kt_bern-set_application_be-ech_instance_be] 1'] = '''<?xml version="1.0" ?>
<ns1:delivery xmlns:ns1="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0129/5" xmlns:ns4="http://www.ech.ch/xmlns/eCH-0010/6" xmlns:ns5="http://www.ech.ch/xmlns/eCH-0007/6" xmlns:ns6="http://www.ech.ch/xmlns/eCH-0147/T0/1" xmlns:ns7="http://www.ech.ch/xmlns/eCH-0039/2" xmlns:ns8="http://www.ech.ch/xmlns/eCH-0044/4" xmlns:ns9="http://www.ech.ch/xmlns/eCH-0097/2">
\t<ns1:deliveryHeader>
\t\t<ns2:senderId>https://ebau.apps.be.ch/</ns2:senderId>
\t\t<ns2:messageId><!-- MESSAGE_ID --></ns2:messageId>
\t\t<ns2:messageType>5200000</ns2:messageType>
\t\t<ns2:sendingApplication>
\t\t\t<ns2:manufacturer>Adfinis AG</ns2:manufacturer>
\t\t\t<ns2:product>camac</ns2:product>
\t\t\t<ns2:productVersion><!-- VERSION --></ns2:productVersion>
\t\t</ns2:sendingApplication>
\t\t<ns2:subject>Einfache Vorabklärung</ns2:subject>
\t\t<ns2:messageDate>2022-06-03T00:00:00Z</ns2:messageDate>
\t\t<ns2:action>1</ns2:action>
\t\t<ns2:testDeliveryFlag>true</ns2:testDeliveryFlag>
\t</ns1:deliveryHeader>
\t<ns1:eventBaseDelivery>
\t\t<ns1:planningPermissionApplicationInformation>
\t\t\t<ns1:planningPermissionApplication>
\t\t\t\t<ns1:planningPermissionApplicationIdentification>
\t\t\t\t\t<ns1:localID>
\t\t\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t\t\t<ns3:Id>2020-1</ns3:Id>
\t\t\t\t\t</ns1:localID>
\t\t\t\t\t<ns1:otherID>
\t\t\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t\t\t<ns3:Id>2020-1</ns3:Id>
\t\t\t\t\t</ns1:otherID>
\t\t\t\t\t<ns1:dossierIdentification><!-- INSTANCE_ID --></ns1:dossierIdentification>
\t\t\t\t</ns1:planningPermissionApplicationIdentification>
\t\t\t\t<ns1:description>Testvorhaben</ns1:description>
\t\t\t\t<ns1:applicationType>Einfache Vorabklärung</ns1:applicationType>
\t\t\t\t<ns1:intendedPurpose>None</ns1:intendedPurpose>
\t\t\t\t<ns1:parkingLotsYesNo>false</ns1:parkingLotsYesNo>
\t\t\t\t<ns1:namedMetaData>
\t\t\t\t\t<ns3:metaDataName>status</ns3:metaDataName>
\t\t\t\t\t<ns3:metaDataValue>David Rangel</ns3:metaDataValue>
\t\t\t\t</ns1:namedMetaData>
\t\t\t\t<ns1:locationAddress>
\t\t\t\t\t<ns4:street>unknown</ns4:street>
\t\t\t\t\t<ns4:houseNumber>0</ns4:houseNumber>
\t\t\t\t\t<ns4:town>unknown</ns4:town>
\t\t\t\t\t<ns4:swissZipCode>9999</ns4:swissZipCode>
\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t</ns4:country>
\t\t\t\t</ns1:locationAddress>
\t\t\t\t<ns1:realestateInformation>
\t\t\t\t\t<ns1:realestate>
\t\t\t\t\t\t<ns3:realestateIdentification>
\t\t\t\t\t\t\t<ns3:number>1586</ns3:number>
\t\t\t\t\t\t</ns3:realestateIdentification>
\t\t\t\t\t\t<ns3:realestateType>8</ns3:realestateType>
\t\t\t\t\t\t<ns3:coordinates>
\t\t\t\t\t\t\t<ns3:LV95>
\t\t\t\t\t\t\t\t<ns3:east>2480000.0</ns3:east>
\t\t\t\t\t\t\t\t<ns3:north>1070000.0</ns3:north>
\t\t\t\t\t\t\t\t<ns3:originOfCoordinates>904</ns3:originOfCoordinates>
\t\t\t\t\t\t\t</ns3:LV95>
\t\t\t\t\t\t</ns3:coordinates>
\t\t\t\t\t</ns1:realestate>
\t\t\t\t\t<ns1:municipality>
\t\t\t\t\t\t<ns5:municipalityName>Testgemeinde</ns5:municipalityName>
\t\t\t\t\t\t<ns5:cantonAbbreviation>BE</ns5:cantonAbbreviation>
\t\t\t\t\t</ns1:municipality>
\t\t\t\t\t<ns1:buildingInformation>
\t\t\t\t\t\t<ns1:building>
\t\t\t\t\t\t\t<ns3:buildingCategory>1040</ns3:buildingCategory>
\t\t\t\t\t\t</ns1:building>
\t\t\t\t\t</ns1:buildingInformation>
\t\t\t\t\t<ns1:owner>
\t\t\t\t\t\t<ns1:ownerAdress>
\t\t\t\t\t\t\t<ns4:person>
\t\t\t\t\t\t\t\t<ns4:firstName>Testvorname</ns4:firstName>
\t\t\t\t\t\t\t\t<ns4:lastName>Testname</ns4:lastName>
\t\t\t\t\t\t\t</ns4:person>
\t\t\t\t\t\t\t<ns4:addressInformation>
\t\t\t\t\t\t\t\t<ns4:street>Teststrasse</ns4:street>
\t\t\t\t\t\t\t\t<ns4:houseNumber>None</ns4:houseNumber>
\t\t\t\t\t\t\t\t<ns4:town>Testort</ns4:town>
\t\t\t\t\t\t\t\t<ns4:swissZipCode>9999</ns4:swissZipCode>
\t\t\t\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t\t\t\t</ns4:country>
\t\t\t\t\t\t\t</ns4:addressInformation>
\t\t\t\t\t\t</ns1:ownerAdress>
\t\t\t\t\t</ns1:owner>
\t\t\t\t</ns1:realestateInformation>
\t\t\t\t<ns1:constructionProjectInformation>
\t\t\t\t\t<ns1:constructionProject>
\t\t\t\t\t\t<ns3:status>6701</ns3:status>
\t\t\t\t\t\t<ns3:description>Testvorhaben</ns3:description>
\t\t\t\t\t</ns1:constructionProject>
\t\t\t\t\t<ns1:municipality>
\t\t\t\t\t\t<ns5:municipalityName>Testgemeinde</ns5:municipalityName>
\t\t\t\t\t\t<ns5:cantonAbbreviation>BE</ns5:cantonAbbreviation>
\t\t\t\t\t</ns1:municipality>
\t\t\t\t</ns1:constructionProjectInformation>
\t\t\t\t<ns1:document>
\t\t\t\t\t<ns6:uuid>00000000-0000-0000-0000-000000000000</ns6:uuid>
\t\t\t\t\t<ns6:titles>
\t\t\t\t\t\t<ns7:title>dummy</ns7:title>
\t\t\t\t\t</ns6:titles>
\t\t\t\t\t<ns6:status>signed</ns6:status>
\t\t\t\t\t<ns6:files>
\t\t\t\t\t\t<ns6:file>
\t\t\t\t\t\t\t<ns6:pathFileName>unknown</ns6:pathFileName>
\t\t\t\t\t\t\t<ns6:mimeType>unknown</ns6:mimeType>
\t\t\t\t\t\t</ns6:file>
\t\t\t\t\t</ns6:files>
\t\t\t\t</ns1:document>
\t\t\t</ns1:planningPermissionApplication>
\t\t\t<ns1:relationshipToPerson>
\t\t\t\t<ns1:role>applicant</ns1:role>
\t\t\t\t<ns1:person>
\t\t\t\t\t<ns3:identification>
\t\t\t\t\t\t<ns3:personIdentification>
\t\t\t\t\t\t\t<ns8:officialName>Testname</ns8:officialName>
\t\t\t\t\t\t\t<ns8:firstName>Testvorname</ns8:firstName>
\t\t\t\t\t\t</ns3:personIdentification>
\t\t\t\t\t</ns3:identification>
\t\t\t\t\t<ns3:address>
\t\t\t\t\t\t<ns4:street>Teststrasse</ns4:street>
\t\t\t\t\t\t<ns4:houseNumber>None</ns4:houseNumber>
\t\t\t\t\t\t<ns4:town>Testort</ns4:town>
\t\t\t\t\t\t<ns4:swissZipCode>9999</ns4:swissZipCode>
\t\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t\t</ns4:country>
\t\t\t\t\t</ns3:address>
\t\t\t\t</ns1:person>
\t\t\t</ns1:relationshipToPerson>
\t\t\t<ns1:decisionAuthority>
\t\t\t\t<ns1:decisionAuthority>
\t\t\t\t\t<ns3:buildingAuthorityIdentificationType>
\t\t\t\t\t\t<ns9:uid>
\t\t\t\t\t\t\t<ns9:uidOrganisationIdCategorie>CHE</ns9:uidOrganisationIdCategorie>
\t\t\t\t\t\t\t<ns9:uidOrganisationId>123123123</ns9:uidOrganisationId>
\t\t\t\t\t\t</ns9:uid>
\t\t\t\t\t\t<ns9:localOrganisationId>
\t\t\t\t\t\t\t<ns9:organisationIdCategory>ebaube</ns9:organisationIdCategory>
\t\t\t\t\t\t\t<ns9:organisationId><!-- ORGANISATION_ID --></ns9:organisationId>
\t\t\t\t\t\t</ns9:localOrganisationId>
\t\t\t\t\t\t<ns9:organisationName>Leitbehörde Burgdorf</ns9:organisationName>
\t\t\t\t\t\t<ns9:legalForm>0223</ns9:legalForm>
\t\t\t\t\t</ns3:buildingAuthorityIdentificationType>
\t\t\t\t\t<ns3:address>
\t\t\t\t\t\t<ns4:street>Teststrasse 23</ns4:street>
\t\t\t\t\t\t<ns4:town>Burgdorf</ns4:town>
\t\t\t\t\t\t<ns4:swissZipCode>3400</ns4:swissZipCode>
\t\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t\t</ns4:country>
\t\t\t\t\t</ns3:address>
\t\t\t\t</ns1:decisionAuthority>
\t\t\t</ns1:decisionAuthority>
\t\t\t<ns1:entryOffice>
\t\t\t\t<ns1:entryOfficeIdentification>
\t\t\t\t\t<ns9:uid>
\t\t\t\t\t\t<ns9:uidOrganisationIdCategorie>CHE</ns9:uidOrganisationIdCategorie>
\t\t\t\t\t\t<ns9:uidOrganisationId>123123123</ns9:uidOrganisationId>
\t\t\t\t\t</ns9:uid>
\t\t\t\t\t<ns9:localOrganisationId>
\t\t\t\t\t\t<ns9:organisationIdCategory>ebaube</ns9:organisationIdCategory>
\t\t\t\t\t\t<ns9:organisationId><!-- ORGANISATION_ID --></ns9:organisationId>
\t\t\t\t\t</ns9:localOrganisationId>
\t\t\t\t\t<ns9:organisationName>Leitbehörde Burgdorf</ns9:organisationName>
\t\t\t\t\t<ns9:legalForm>0223</ns9:legalForm>
\t\t\t\t</ns1:entryOfficeIdentification>
\t\t\t\t<ns1:municipality>
\t\t\t\t\t<ns5:municipalityName>Burgdorf</ns5:municipalityName>
\t\t\t\t\t<ns5:cantonAbbreviation>BE</ns5:cantonAbbreviation>
\t\t\t\t</ns1:municipality>
\t\t\t</ns1:entryOffice>
\t\t</ns1:planningPermissionApplicationInformation>
\t</ns1:eventBaseDelivery>
</ns1:delivery>
'''

snapshots['test_generate_delivery[kt_schwyz-set_application_sz-ech_instance_sz] 1'] = '''<?xml version="1.0" ?>
<ns1:delivery xmlns:ns1="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0129/5" xmlns:ns4="http://www.ech.ch/xmlns/eCH-0010/6" xmlns:ns5="http://www.ech.ch/xmlns/eCH-0007/6" xmlns:ns6="http://www.ech.ch/xmlns/eCH-0147/T0/1" xmlns:ns7="http://www.ech.ch/xmlns/eCH-0039/2" xmlns:ns8="http://www.ech.ch/xmlns/eCH-0097/2" xmlns:ns9="http://www.ech.ch/xmlns/eCH-0044/4">
\t<ns1:deliveryHeader>
\t\t<ns2:senderId>https://behoerden.ebau-sz.ch/</ns2:senderId>
\t\t<ns2:messageId><!-- MESSAGE_ID --></ns2:messageId>
\t\t<ns2:messageType>5200000</ns2:messageType>
\t\t<ns2:sendingApplication>
\t\t\t<ns2:manufacturer>Adfinis AG</ns2:manufacturer>
\t\t\t<ns2:product>camac</ns2:product>
\t\t\t<ns2:productVersion><!-- VERSION --></ns2:productVersion>
\t\t</ns2:sendingApplication>
\t\t<ns2:subject>Einfache Vorabklärung</ns2:subject>
\t\t<ns2:messageDate>2022-06-03T00:00:00Z</ns2:messageDate>
\t\t<ns2:action>1</ns2:action>
\t\t<ns2:testDeliveryFlag>true</ns2:testDeliveryFlag>
\t</ns1:deliveryHeader>
\t<ns1:eventBaseDelivery>
\t\t<ns1:planningPermissionApplicationInformation>
\t\t\t<ns1:planningPermissionApplication>
\t\t\t\t<ns1:planningPermissionApplicationIdentification>
\t\t\t\t\t<ns1:localID>
\t\t\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t\t\t<ns3:Id>TEST-8403-22-001</ns3:Id>
\t\t\t\t\t</ns1:localID>
\t\t\t\t\t<ns1:otherID>
\t\t\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t\t\t<ns3:Id>TEST-8403-22-001</ns3:Id>
\t\t\t\t\t</ns1:otherID>
\t\t\t\t\t<ns1:dossierIdentification><!-- INSTANCE_ID --></ns1:dossierIdentification>
\t\t\t\t</ns1:planningPermissionApplicationIdentification>
\t\t\t\t<ns1:description>None</ns1:description>
\t\t\t\t<ns1:applicationType>Christopher Foster</ns1:applicationType>
\t\t\t\t<ns1:remark>None</ns1:remark>
\t\t\t\t<ns1:proceedingType>baubewilligung</ns1:proceedingType>
\t\t\t\t<ns1:profilingYesNo>false</ns1:profilingYesNo>
\t\t\t\t<ns1:intendedPurpose>None</ns1:intendedPurpose>
\t\t\t\t<ns1:namedMetaData>
\t\t\t\t\t<ns3:metaDataName>status</ns3:metaDataName>
\t\t\t\t\t<ns3:metaDataValue>David Rangel</ns3:metaDataValue>
\t\t\t\t</ns1:namedMetaData>
\t\t\t\t<ns1:locationAddress>
\t\t\t\t\t<ns4:street>None</ns4:street>
\t\t\t\t\t<ns4:houseNumber>.</ns4:houseNumber>
\t\t\t\t\t<ns4:town>None</ns4:town>
\t\t\t\t\t<ns4:swissZipCode>9999</ns4:swissZipCode>
\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t</ns4:country>
\t\t\t\t</ns1:locationAddress>
\t\t\t\t<ns1:realestateInformation>
\t\t\t\t\t<ns1:realestate>
\t\t\t\t\t\t<ns3:realestateIdentification>
\t\t\t\t\t\t\t<ns3:number>0</ns3:number>
\t\t\t\t\t\t</ns3:realestateIdentification>
\t\t\t\t\t\t<ns3:realestateType>8</ns3:realestateType>
\t\t\t\t\t</ns1:realestate>
\t\t\t\t\t<ns1:municipality>
\t\t\t\t\t\t<ns5:municipalityName>Elizabethburgh</ns5:municipalityName>
\t\t\t\t\t\t<ns5:cantonAbbreviation>SZ</ns5:cantonAbbreviation>
\t\t\t\t\t</ns1:municipality>
\t\t\t\t\t<ns1:owner>
\t\t\t\t\t\t<ns1:ownerAdress>
\t\t\t\t\t\t\t<ns4:person>
\t\t\t\t\t\t\t\t<ns4:firstName>unknown</ns4:firstName>
\t\t\t\t\t\t\t\t<ns4:lastName>unknown</ns4:lastName>
\t\t\t\t\t\t\t</ns4:person>
\t\t\t\t\t\t\t<ns4:addressInformation>
\t\t\t\t\t\t\t\t<ns4:street>unknown</ns4:street>
\t\t\t\t\t\t\t\t<ns4:houseNumber>0</ns4:houseNumber>
\t\t\t\t\t\t\t\t<ns4:town>unknown</ns4:town>
\t\t\t\t\t\t\t\t<ns4:swissZipCode>9999</ns4:swissZipCode>
\t\t\t\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t\t\t\t</ns4:country>
\t\t\t\t\t\t\t</ns4:addressInformation>
\t\t\t\t\t\t</ns1:ownerAdress>
\t\t\t\t\t</ns1:owner>
\t\t\t\t</ns1:realestateInformation>
\t\t\t\t<ns1:document>
\t\t\t\t\t<ns6:uuid>42b55f5f-3d79-4f29-af7b-a2377283a139</ns6:uuid>
\t\t\t\t\t<ns6:titles>
\t\t\t\t\t\t<ns7:title>able</ns7:title>
\t\t\t\t\t</ns6:titles>
\t\t\t\t\t<ns6:status>signed</ns6:status>
\t\t\t\t\t<ns6:files>
\t\t\t\t\t\t<ns6:file>
\t\t\t\t\t\t\t<ns6:pathFileName>http://ebau.local/api/v1/attachments/files/?attachments=<!-- ATTACHMENT_ID --></ns6:pathFileName>
\t\t\t\t\t\t\t<ns6:mimeType>multipart/form-data</ns6:mimeType>
\t\t\t\t\t\t</ns6:file>
\t\t\t\t\t</ns6:files>
\t\t\t\t\t<ns6:documentKind/>
\t\t\t\t</ns1:document>
\t\t\t\t<ns1:referencedPlanningPermissionApplication>
\t\t\t\t\t<ns1:localID>
\t\t\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t\t\t<ns3:Id>TEST-8403-22-001</ns3:Id>
\t\t\t\t\t</ns1:localID>
\t\t\t\t\t<ns1:otherID>
\t\t\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t\t\t<ns3:Id>TEST-8403-22-001</ns3:Id>
\t\t\t\t\t</ns1:otherID>
\t\t\t\t\t<ns1:dossierIdentification><!-- INSTANCE_ID --></ns1:dossierIdentification>
\t\t\t\t</ns1:referencedPlanningPermissionApplication>
\t\t\t</ns1:planningPermissionApplication>
\t\t\t<ns1:relationshipToPerson>
\t\t\t\t<ns1:role>applicant</ns1:role>
\t\t\t\t<ns1:person>
\t\t\t\t\t<ns3:identification>
\t\t\t\t\t\t<ns3:organisationIdentification>
\t\t\t\t\t\t\t<ns8:uid>
\t\t\t\t\t\t\t\t<ns8:uidOrganisationIdCategorie>CHE</ns8:uidOrganisationIdCategorie>
\t\t\t\t\t\t\t\t<ns8:uidOrganisationId>123123123</ns8:uidOrganisationId>
\t\t\t\t\t\t\t</ns8:uid>
\t\t\t\t\t\t\t<ns8:localOrganisationId>
\t\t\t\t\t\t\t\t<ns8:organisationIdCategory>unknown</ns8:organisationIdCategory>
\t\t\t\t\t\t\t\t<ns8:organisationId><!-- ORGANISATION_ID --></ns8:organisationId>
\t\t\t\t\t\t\t</ns8:localOrganisationId>
\t\t\t\t\t\t\t<ns8:organisationName>White Group</ns8:organisationName>
\t\t\t\t\t\t\t<ns8:organisationAdditionalName>Heather Marsh</ns8:organisationAdditionalName>
\t\t\t\t\t\t\t<ns8:legalForm>0223</ns8:legalForm>
\t\t\t\t\t\t</ns3:organisationIdentification>
\t\t\t\t\t</ns3:identification>
\t\t\t\t\t<ns3:address>
\t\t\t\t\t\t<ns4:street>Miller Centers</ns4:street>
\t\t\t\t\t\t<ns4:houseNumber>.</ns4:houseNumber>
\t\t\t\t\t\t<ns4:town>Thomasville</ns4:town>
\t\t\t\t\t\t<ns4:swissZipCode>1816</ns4:swissZipCode>
\t\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t\t</ns4:country>
\t\t\t\t\t</ns3:address>
\t\t\t\t</ns1:person>
\t\t\t</ns1:relationshipToPerson>
\t\t\t<ns1:relationshipToPerson>
\t\t\t\t<ns1:role>contact</ns1:role>
\t\t\t\t<ns1:person>
\t\t\t\t\t<ns3:identification>
\t\t\t\t\t\t<ns3:personIdentification>
\t\t\t\t\t\t\t<ns9:officialName>Liu</ns9:officialName>
\t\t\t\t\t\t\t<ns9:firstName>Jessica</ns9:firstName>
\t\t\t\t\t\t</ns3:personIdentification>
\t\t\t\t\t</ns3:identification>
\t\t\t\t\t<ns3:address>
\t\t\t\t\t\t<ns4:street>Scott Ridge</ns4:street>
\t\t\t\t\t\t<ns4:houseNumber>.</ns4:houseNumber>
\t\t\t\t\t\t<ns4:town>Lake Williamchester</ns4:town>
\t\t\t\t\t\t<ns4:swissZipCode>5731</ns4:swissZipCode>
\t\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t\t</ns4:country>
\t\t\t\t\t</ns3:address>
\t\t\t\t</ns1:person>
\t\t\t</ns1:relationshipToPerson>
\t\t\t<ns1:relationshipToPerson>
\t\t\t\t<ns1:role>project author</ns1:role>
\t\t\t\t<ns1:person>
\t\t\t\t\t<ns3:identification>
\t\t\t\t\t\t<ns3:personIdentification>
\t\t\t\t\t\t\t<ns9:officialName>Gilbert</ns9:officialName>
\t\t\t\t\t\t\t<ns9:firstName>Crystal</ns9:firstName>
\t\t\t\t\t\t</ns3:personIdentification>
\t\t\t\t\t</ns3:identification>
\t\t\t\t\t<ns3:address>
\t\t\t\t\t\t<ns4:street>Carl Port</ns4:street>
\t\t\t\t\t\t<ns4:houseNumber>.</ns4:houseNumber>
\t\t\t\t\t\t<ns4:town>Brownstad</ns4:town>
\t\t\t\t\t\t<ns4:swissZipCode>9394</ns4:swissZipCode>
\t\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t\t</ns4:country>
\t\t\t\t\t</ns3:address>
\t\t\t\t</ns1:person>
\t\t\t</ns1:relationshipToPerson>
\t\t\t<ns1:relationshipToPerson>
\t\t\t\t<ns1:role>landowner</ns1:role>
\t\t\t\t<ns1:person>
\t\t\t\t\t<ns3:identification>
\t\t\t\t\t\t<ns3:personIdentification>
\t\t\t\t\t\t\t<ns9:officialName>Lloyd</ns9:officialName>
\t\t\t\t\t\t\t<ns9:firstName>Ian</ns9:firstName>
\t\t\t\t\t\t</ns3:personIdentification>
\t\t\t\t\t</ns3:identification>
\t\t\t\t\t<ns3:address>
\t\t\t\t\t\t<ns4:street>Ryan Burgs</ns4:street>
\t\t\t\t\t\t<ns4:houseNumber>.</ns4:houseNumber>
\t\t\t\t\t\t<ns4:town>East Charlesburgh</ns4:town>
\t\t\t\t\t\t<ns4:swissZipCode>5416</ns4:swissZipCode>
\t\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t\t</ns4:country>
\t\t\t\t\t</ns3:address>
\t\t\t\t</ns1:person>
\t\t\t</ns1:relationshipToPerson>
\t\t\t<ns1:decisionAuthority>
\t\t\t\t<ns1:decisionAuthority>
\t\t\t\t\t<ns3:buildingAuthorityIdentificationType>
\t\t\t\t\t\t<ns8:uid>
\t\t\t\t\t\t\t<ns8:uidOrganisationIdCategorie>CHE</ns8:uidOrganisationIdCategorie>
\t\t\t\t\t\t\t<ns8:uidOrganisationId>123123123</ns8:uidOrganisationId>
\t\t\t\t\t\t</ns8:uid>
\t\t\t\t\t\t<ns8:localOrganisationId>
\t\t\t\t\t\t\t<ns8:organisationIdCategory>ebausz</ns8:organisationIdCategory>
\t\t\t\t\t\t\t<ns8:organisationId><!-- ORGANISATION_ID --></ns8:organisationId>
\t\t\t\t\t\t</ns8:localOrganisationId>
\t\t\t\t\t\t<ns8:organisationName>Christine Powers</ns8:organisationName>
\t\t\t\t\t\t<ns8:legalForm>0223</ns8:legalForm>
\t\t\t\t\t</ns3:buildingAuthorityIdentificationType>
\t\t\t\t\t<ns3:address>
\t\t\t\t\t\t<ns4:street>None</ns4:street>
\t\t\t\t\t\t<ns4:town>unknown</ns4:town>
\t\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t\t</ns4:country>
\t\t\t\t\t</ns3:address>
\t\t\t\t</ns1:decisionAuthority>
\t\t\t</ns1:decisionAuthority>
\t\t\t<ns1:entryOffice>
\t\t\t\t<ns1:entryOfficeIdentification>
\t\t\t\t\t<ns8:uid>
\t\t\t\t\t\t<ns8:uidOrganisationIdCategorie>CHE</ns8:uidOrganisationIdCategorie>
\t\t\t\t\t\t<ns8:uidOrganisationId>123123123</ns8:uidOrganisationId>
\t\t\t\t\t</ns8:uid>
\t\t\t\t\t<ns8:localOrganisationId>
\t\t\t\t\t\t<ns8:organisationIdCategory>ebausz</ns8:organisationIdCategory>
\t\t\t\t\t\t<ns8:organisationId><!-- ORGANISATION_ID --></ns8:organisationId>
\t\t\t\t\t</ns8:localOrganisationId>
\t\t\t\t\t<ns8:organisationName>Christine Powers</ns8:organisationName>
\t\t\t\t\t<ns8:legalForm>0223</ns8:legalForm>
\t\t\t\t</ns1:entryOfficeIdentification>
\t\t\t\t<ns1:municipality>
\t\t\t\t\t<ns5:municipalityName>unknown</ns5:municipalityName>
\t\t\t\t\t<ns5:cantonAbbreviation>SZ</ns5:cantonAbbreviation>
\t\t\t\t</ns1:municipality>
\t\t\t</ns1:entryOffice>
\t\t</ns1:planningPermissionApplicationInformation>
\t</ns1:eventBaseDelivery>
</ns1:delivery>
'''
