# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_accompanying_report_event_handler[False] 1'] = '''<?xml version="1.0" ?>
<ns1:delivery xmlns:ns1="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0129/5" xmlns:ns4="http://www.ech.ch/xmlns/eCH-0147/T0/1" xmlns:ns5="http://www.ech.ch/xmlns/eCH-0039/2">
\t<ns1:deliveryHeader>
\t\t<ns2:senderId>https://ebau.apps.be.ch/</ns2:senderId>
\t\t<ns2:messageId><!-- MESSAGE_ID --></ns2:messageId>
\t\t<ns2:messageType>5100004</ns2:messageType>
\t\t<ns2:sendingApplication>
\t\t\t<ns2:manufacturer>Adfinis AG</ns2:manufacturer>
\t\t\t<ns2:product>camac</ns2:product>
\t\t\t<ns2:productVersion><!-- VERSION --></ns2:productVersion>
\t\t</ns2:sendingApplication>
\t\t<ns2:subject>accompanying report</ns2:subject>
\t\t<ns2:messageDate>2022-06-03T00:00:00Z</ns2:messageDate>
\t\t<ns2:action>1</ns2:action>
\t\t<ns2:testDeliveryFlag>true</ns2:testDeliveryFlag>
\t</ns1:deliveryHeader>
\t<ns1:eventAccompanyingReport>
\t\t<ns1:eventType>accompanying report</ns1:eventType>
\t\t<ns1:planningPermissionApplicationIdentification>
\t\t\t<ns1:localID>
\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t<ns3:Id>2020-1</ns3:Id>
\t\t\t</ns1:localID>
\t\t\t<ns1:otherID>
\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t<ns3:Id>2020-1</ns3:Id>
\t\t\t</ns1:otherID>
\t\t\t<ns1:dossierIdentification><!-- INSTANCE_ID --></ns1:dossierIdentification>
\t\t</ns1:planningPermissionApplicationIdentification>
\t\t<ns1:document>
\t\t\t<ns4:uuid>663448f0-a6d9-44da-a1d9-8890fdc6912c</ns4:uuid>
\t\t\t<ns4:titles>
\t\t\t\t<ns5:title>parent</ns5:title>
\t\t\t</ns4:titles>
\t\t\t<ns4:status>signed</ns4:status>
\t\t\t<ns4:files>
\t\t\t\t<ns4:file>
\t\t\t\t\t<ns4:pathFileName>http://ebau.local/api/v1/attachments/files/?attachments=<!-- ATTACHMENT_ID --></ns4:pathFileName>
\t\t\t\t\t<ns4:mimeType>multipart/related</ns4:mimeType>
\t\t\t\t</ns4:file>
\t\t\t</ns4:files>
\t\t\t<ns4:documentKind>Paul Mitchell</ns4:documentKind>
\t\t</ns1:document>
\t\t<ns1:document>
\t\t\t<ns4:uuid>a21a0d75-7490-4e26-8022-f6665cf7716d</ns4:uuid>
\t\t\t<ns4:titles>
\t\t\t\t<ns5:title>child</ns5:title>
\t\t\t</ns4:titles>
\t\t\t<ns4:status>signed</ns4:status>
\t\t\t<ns4:files>
\t\t\t\t<ns4:file>
\t\t\t\t\t<ns4:pathFileName>http://ebau.local/api/v1/attachments/files/?attachments=<!-- ATTACHMENT_ID --></ns4:pathFileName>
\t\t\t\t\t<ns4:mimeType>audio/L24</ns4:mimeType>
\t\t\t\t</ns4:file>
\t\t\t</ns4:files>
\t\t\t<ns4:documentKind>Paul Mitchell</ns4:documentKind>
\t\t</ns1:document>
\t</ns1:eventAccompanyingReport>
</ns1:delivery>
'''

snapshots['test_accompanying_report_event_handler[True] 1'] = '''<?xml version="1.0" ?>
<ns1:delivery xmlns:ns1="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0129/5" xmlns:ns4="http://www.ech.ch/xmlns/eCH-0147/T0/1" xmlns:ns5="http://www.ech.ch/xmlns/eCH-0039/2">
\t<ns1:deliveryHeader>
\t\t<ns2:senderId>https://ebau.apps.be.ch/</ns2:senderId>
\t\t<ns2:messageId><!-- MESSAGE_ID --></ns2:messageId>
\t\t<ns2:messageType>5100004</ns2:messageType>
\t\t<ns2:sendingApplication>
\t\t\t<ns2:manufacturer>Adfinis AG</ns2:manufacturer>
\t\t\t<ns2:product>camac</ns2:product>
\t\t\t<ns2:productVersion><!-- VERSION --></ns2:productVersion>
\t\t</ns2:sendingApplication>
\t\t<ns2:subject>accompanying report</ns2:subject>
\t\t<ns2:messageDate>2022-06-03T00:00:00Z</ns2:messageDate>
\t\t<ns2:action>1</ns2:action>
\t\t<ns2:testDeliveryFlag>true</ns2:testDeliveryFlag>
\t</ns1:deliveryHeader>
\t<ns1:eventAccompanyingReport>
\t\t<ns1:eventType>accompanying report</ns1:eventType>
\t\t<ns1:planningPermissionApplicationIdentification>
\t\t\t<ns1:localID>
\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t<ns3:Id>2020-1</ns3:Id>
\t\t\t</ns1:localID>
\t\t\t<ns1:otherID>
\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t<ns3:Id>2020-1</ns3:Id>
\t\t\t</ns1:otherID>
\t\t\t<ns1:dossierIdentification><!-- INSTANCE_ID --></ns1:dossierIdentification>
\t\t</ns1:planningPermissionApplicationIdentification>
\t\t<ns1:document>
\t\t\t<ns4:uuid>663448f0-a6d9-44da-a1d9-8890fdc6912c</ns4:uuid>
\t\t\t<ns4:titles>
\t\t\t\t<ns5:title>parent</ns5:title>
\t\t\t</ns4:titles>
\t\t\t<ns4:status>signed</ns4:status>
\t\t\t<ns4:files>
\t\t\t\t<ns4:file>
\t\t\t\t\t<ns4:pathFileName>http://ebau.local/api/v1/attachments/files/?attachments=<!-- ATTACHMENT_ID --></ns4:pathFileName>
\t\t\t\t\t<ns4:mimeType>multipart/related</ns4:mimeType>
\t\t\t\t</ns4:file>
\t\t\t</ns4:files>
\t\t\t<ns4:documentKind>Paul Mitchell</ns4:documentKind>
\t\t</ns1:document>
\t\t<ns1:document>
\t\t\t<ns4:uuid>a21a0d75-7490-4e26-8022-f6665cf7716d</ns4:uuid>
\t\t\t<ns4:titles>
\t\t\t\t<ns5:title>child</ns5:title>
\t\t\t</ns4:titles>
\t\t\t<ns4:status>signed</ns4:status>
\t\t\t<ns4:files>
\t\t\t\t<ns4:file>
\t\t\t\t\t<ns4:pathFileName>http://ebau.local/api/v1/attachments/files/?attachments=<!-- ATTACHMENT_ID --></ns4:pathFileName>
\t\t\t\t\t<ns4:mimeType>audio/L24</ns4:mimeType>
\t\t\t\t</ns4:file>
\t\t\t</ns4:files>
\t\t\t<ns4:documentKind>Paul Mitchell</ns4:documentKind>
\t\t</ns1:document>
\t\t<ns1:remark>lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum l…</ns1:remark>
\t\t<ns1:ancillaryClauses>nebenbestimmung&amp;#13;&amp;#10;blablabla&amp;#13;&amp;#10;blu; yeah</ns1:ancillaryClauses>
\t</ns1:eventAccompanyingReport>
</ns1:delivery>
'''

snapshots['test_event_handlers[ChangeResponsibility] 1'] = '''<?xml version="1.0" ?>
<ns1:delivery xmlns:ns1="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0129/5" xmlns:ns4="http://www.ech.ch/xmlns/eCH-0097/2" xmlns:ns5="http://www.ech.ch/xmlns/eCH-0007/6" xmlns:ns6="http://www.ech.ch/xmlns/eCH-0010/6">
\t<ns1:deliveryHeader>
\t\t<ns2:senderId>https://ebau.apps.be.ch/</ns2:senderId>
\t\t<ns2:messageId><!-- MESSAGE_ID --></ns2:messageId>
\t\t<ns2:messageType>5200005</ns2:messageType>
\t\t<ns2:sendingApplication>
\t\t\t<ns2:manufacturer>Adfinis AG</ns2:manufacturer>
\t\t\t<ns2:product>camac</ns2:product>
\t\t\t<ns2:productVersion><!-- VERSION --></ns2:productVersion>
\t\t</ns2:sendingApplication>
\t\t<ns2:subject>change responsibility</ns2:subject>
\t\t<ns2:messageDate>2022-06-03T00:00:00Z</ns2:messageDate>
\t\t<ns2:action>1</ns2:action>
\t\t<ns2:testDeliveryFlag>true</ns2:testDeliveryFlag>
\t</ns1:deliveryHeader>
\t<ns1:eventChangeResponsibility>
\t\t<ns1:eventType>change responsibility</ns1:eventType>
\t\t<ns1:planningPermissionApplicationIdentification>
\t\t\t<ns1:localID>
\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t<ns3:Id>unknown</ns3:Id>
\t\t\t</ns1:localID>
\t\t\t<ns1:otherID>
\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t<ns3:Id>unknown</ns3:Id>
\t\t\t</ns1:otherID>
\t\t\t<ns1:dossierIdentification><!-- INSTANCE_ID --></ns1:dossierIdentification>
\t\t</ns1:planningPermissionApplicationIdentification>
\t\t<ns1:entryOffice>
\t\t\t<ns1:entryOfficeIdentification>
\t\t\t\t<ns4:uid>
\t\t\t\t\t<ns4:uidOrganisationIdCategorie>CHE</ns4:uidOrganisationIdCategorie>
\t\t\t\t\t<ns4:uidOrganisationId>123123123</ns4:uidOrganisationId>
\t\t\t\t</ns4:uid>
\t\t\t\t<ns4:localOrganisationId>
\t\t\t\t\t<ns4:organisationIdCategory>ebaube</ns4:organisationIdCategory>
\t\t\t\t\t<ns4:organisationId><!-- ORGANISATION_ID --></ns4:organisationId>
\t\t\t\t</ns4:localOrganisationId>
\t\t\t\t<ns4:organisationName>Leitbehörde Burgdorf</ns4:organisationName>
\t\t\t\t<ns4:legalForm>0223</ns4:legalForm>
\t\t\t</ns1:entryOfficeIdentification>
\t\t\t<ns1:municipality>
\t\t\t\t<ns5:municipalityName>Burgdorf</ns5:municipalityName>
\t\t\t\t<ns5:cantonAbbreviation>BE</ns5:cantonAbbreviation>
\t\t\t</ns1:municipality>
\t\t</ns1:entryOffice>
\t\t<ns1:responsibleDecisionAuthority>
\t\t\t<ns1:decisionAuthority>
\t\t\t\t<ns3:buildingAuthorityIdentificationType>
\t\t\t\t\t<ns4:uid>
\t\t\t\t\t\t<ns4:uidOrganisationIdCategorie>CHE</ns4:uidOrganisationIdCategorie>
\t\t\t\t\t\t<ns4:uidOrganisationId>123123123</ns4:uidOrganisationId>
\t\t\t\t\t</ns4:uid>
\t\t\t\t\t<ns4:localOrganisationId>
\t\t\t\t\t\t<ns4:organisationIdCategory>ebaube</ns4:organisationIdCategory>
\t\t\t\t\t\t<ns4:organisationId><!-- ORGANISATION_ID --></ns4:organisationId>
\t\t\t\t\t</ns4:localOrganisationId>
\t\t\t\t\t<ns4:organisationName>Leitbehörde Madiswil</ns4:organisationName>
\t\t\t\t\t<ns4:legalForm>0223</ns4:legalForm>
\t\t\t\t</ns3:buildingAuthorityIdentificationType>
\t\t\t\t<ns3:address>
\t\t\t\t\t<ns6:street>Testweg 5</ns6:street>
\t\t\t\t\t<ns6:town>Madiswil</ns6:town>
\t\t\t\t\t<ns6:swissZipCode>3500</ns6:swissZipCode>
\t\t\t\t\t<ns6:country>
\t\t\t\t\t\t<ns6:countryNameShort>CH</ns6:countryNameShort>
\t\t\t\t\t</ns6:country>
\t\t\t\t</ns3:address>
\t\t\t</ns1:decisionAuthority>
\t\t</ns1:responsibleDecisionAuthority>
\t</ns1:eventChangeResponsibility>
</ns1:delivery>
'''

snapshots['test_event_handlers[Claim] 1'] = '''<?xml version="1.0" ?>
<ns1:delivery xmlns:ns1="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0129/5">
\t<ns1:deliveryHeader>
\t\t<ns2:senderId>https://ebau.apps.be.ch/</ns2:senderId>
\t\t<ns2:messageId><!-- MESSAGE_ID --></ns2:messageId>
\t\t<ns2:messageType>5200004</ns2:messageType>
\t\t<ns2:sendingApplication>
\t\t\t<ns2:manufacturer>Adfinis AG</ns2:manufacturer>
\t\t\t<ns2:product>camac</ns2:product>
\t\t\t<ns2:productVersion><!-- VERSION --></ns2:productVersion>
\t\t</ns2:sendingApplication>
\t\t<ns2:subject>claim</ns2:subject>
\t\t<ns2:messageDate>2022-06-03T00:00:00Z</ns2:messageDate>
\t\t<ns2:action>1</ns2:action>
\t\t<ns2:testDeliveryFlag>true</ns2:testDeliveryFlag>
\t</ns1:deliveryHeader>
\t<ns1:eventRequest>
\t\t<ns1:eventType>claim</ns1:eventType>
\t\t<ns1:planningPermissionApplicationIdentification>
\t\t\t<ns1:localID>
\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t<ns3:Id>unknown</ns3:Id>
\t\t\t</ns1:localID>
\t\t\t<ns1:otherID>
\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t<ns3:Id>unknown</ns3:Id>
\t\t\t</ns1:otherID>
\t\t\t<ns1:dossierIdentification><!-- INSTANCE_ID --></ns1:dossierIdentification>
\t\t</ns1:planningPermissionApplicationIdentification>
\t</ns1:eventRequest>
</ns1:delivery>
'''

snapshots['test_event_handlers[FileSubsequently] 1'] = '''<?xml version="1.0" ?>
<ns1:delivery xmlns:ns1="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0129/5" xmlns:ns4="http://www.ech.ch/xmlns/eCH-0010/6" xmlns:ns5="http://www.ech.ch/xmlns/eCH-0007/6" xmlns:ns6="http://www.ech.ch/xmlns/eCH-0147/T0/1" xmlns:ns7="http://www.ech.ch/xmlns/eCH-0039/2" xmlns:ns8="http://www.ech.ch/xmlns/eCH-0044/4" xmlns:ns9="http://www.ech.ch/xmlns/eCH-0097/2">
\t<ns1:deliveryHeader>
\t\t<ns2:senderId>https://ebau.apps.be.ch/</ns2:senderId>
\t\t<ns2:messageId><!-- MESSAGE_ID --></ns2:messageId>
\t\t<ns2:messageType>5100001</ns2:messageType>
\t\t<ns2:sendingApplication>
\t\t\t<ns2:manufacturer>Adfinis AG</ns2:manufacturer>
\t\t\t<ns2:product>camac</ns2:product>
\t\t\t<ns2:productVersion><!-- VERSION --></ns2:productVersion>
\t\t</ns2:sendingApplication>
\t\t<ns2:subject>Generelles Baugesuch</ns2:subject>
\t\t<ns2:messageDate>2022-06-03T00:00:00Z</ns2:messageDate>
\t\t<ns2:action>1</ns2:action>
\t\t<ns2:testDeliveryFlag>true</ns2:testDeliveryFlag>
\t</ns1:deliveryHeader>
\t<ns1:eventSubmitPlanningPermissionApplication>
\t\t<ns1:eventType>file subsequently</ns1:eventType>
\t\t<ns1:planningPermissionApplication>
\t\t\t<ns1:planningPermissionApplicationIdentification>
\t\t\t\t<ns1:localID>
\t\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t\t<ns3:Id>unknown</ns3:Id>
\t\t\t\t</ns1:localID>
\t\t\t\t<ns1:otherID>
\t\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t\t<ns3:Id>unknown</ns3:Id>
\t\t\t\t</ns1:otherID>
\t\t\t\t<ns1:dossierIdentification><!-- INSTANCE_ID --></ns1:dossierIdentification>
\t\t\t</ns1:planningPermissionApplicationIdentification>
\t\t\t<ns1:description>Beschreibung&amp;#10;Mehr Beschreibung</ns1:description>
\t\t\t<ns1:applicationType>Generelles Baugesuch</ns1:applicationType>
\t\t\t<ns1:remark>Foo bar</ns1:remark>
\t\t\t<ns1:intendedPurpose>Wohnen</ns1:intendedPurpose>
\t\t\t<ns1:parkingLotsYesNo>true</ns1:parkingLotsYesNo>
\t\t\t<ns1:natureRisk>
\t\t\t\t<ns1:riskDesignation>Fliesslawine</ns1:riskDesignation>
\t\t\t\t<ns1:riskExists>true</ns1:riskExists>
\t\t\t</ns1:natureRisk>
\t\t\t<ns1:constructionCost>232323.0</ns1:constructionCost>
\t\t\t<ns1:namedMetaData>
\t\t\t\t<ns3:metaDataName>status</ns3:metaDataName>
\t\t\t\t<ns3:metaDataValue>David Rangel</ns3:metaDataValue>
\t\t\t</ns1:namedMetaData>
\t\t\t<ns1:locationAddress>
\t\t\t\t<ns4:street>Teststrasse</ns4:street>
\t\t\t\t<ns4:houseNumber>23</ns4:houseNumber>
\t\t\t\t<ns4:town>Burgdorf</ns4:town>
\t\t\t\t<ns4:swissZipCode>9999</ns4:swissZipCode>
\t\t\t\t<ns4:country>
\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t</ns4:country>
\t\t\t</ns1:locationAddress>
\t\t\t<ns1:realestateInformation>
\t\t\t\t<ns1:realestate>
\t\t\t\t\t<ns3:realestateIdentification>
\t\t\t\t\t\t<ns3:EGRID>23</ns3:EGRID>
\t\t\t\t\t\t<ns3:number>1586</ns3:number>
\t\t\t\t\t</ns3:realestateIdentification>
\t\t\t\t\t<ns3:realestateType>8</ns3:realestateType>
\t\t\t\t\t<ns3:coordinates>
\t\t\t\t\t\t<ns3:LV95>
\t\t\t\t\t\t\t<ns3:east>2480034.0</ns3:east>
\t\t\t\t\t\t\t<ns3:north>1070500.0</ns3:north>
\t\t\t\t\t\t\t<ns3:originOfCoordinates>904</ns3:originOfCoordinates>
\t\t\t\t\t\t</ns3:LV95>
\t\t\t\t\t</ns3:coordinates>
\t\t\t\t</ns1:realestate>
\t\t\t\t<ns1:municipality>
\t\t\t\t\t<ns5:municipalityName>2</ns5:municipalityName>
\t\t\t\t\t<ns5:cantonAbbreviation>BE</ns5:cantonAbbreviation>
\t\t\t\t</ns1:municipality>
\t\t\t\t<ns1:buildingInformation>
\t\t\t\t\t<ns1:building>
\t\t\t\t\t\t<ns3:EGID>23</ns3:EGID>
\t\t\t\t\t\t<ns3:numberOfFloors>23</ns3:numberOfFloors>
\t\t\t\t\t\t<ns3:buildingCategory>1040</ns3:buildingCategory>
\t\t\t\t\t\t<ns3:civilDefenseShelter>true</ns3:civilDefenseShelter>
\t\t\t\t\t</ns1:building>
\t\t\t\t</ns1:buildingInformation>
\t\t\t\t<ns1:owner>
\t\t\t\t\t<ns1:ownerAdress>
\t\t\t\t\t\t<ns4:person>
\t\t\t\t\t\t\t<ns4:firstName>Winston</ns4:firstName>
\t\t\t\t\t\t\t<ns4:lastName>Smith</ns4:lastName>
\t\t\t\t\t\t</ns4:person>
\t\t\t\t\t\t<ns4:addressInformation>
\t\t\t\t\t\t\t<ns4:street>Teststrasse</ns4:street>
\t\t\t\t\t\t\t<ns4:houseNumber>23</ns4:houseNumber>
\t\t\t\t\t\t\t<ns4:town>Burgdorf</ns4:town>
\t\t\t\t\t\t\t<ns4:swissZipCode>2323</ns4:swissZipCode>
\t\t\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t\t\t</ns4:country>
\t\t\t\t\t\t</ns4:addressInformation>
\t\t\t\t\t</ns1:ownerAdress>
\t\t\t\t</ns1:owner>
\t\t\t</ns1:realestateInformation>
\t\t\t<ns1:realestateInformation>
\t\t\t\t<ns1:realestate>
\t\t\t\t\t<ns3:realestateIdentification>
\t\t\t\t\t\t<ns3:EGRID>24</ns3:EGRID>
\t\t\t\t\t\t<ns3:number>1587</ns3:number>
\t\t\t\t\t</ns3:realestateIdentification>
\t\t\t\t\t<ns3:realestateType>8</ns3:realestateType>
\t\t\t\t\t<ns3:coordinates>
\t\t\t\t\t\t<ns3:LV95>
\t\t\t\t\t\t\t<ns3:east>2480035.0</ns3:east>
\t\t\t\t\t\t\t<ns3:north>1070600.0</ns3:north>
\t\t\t\t\t\t\t<ns3:originOfCoordinates>904</ns3:originOfCoordinates>
\t\t\t\t\t\t</ns3:LV95>
\t\t\t\t\t</ns3:coordinates>
\t\t\t\t</ns1:realestate>
\t\t\t\t<ns1:municipality>
\t\t\t\t\t<ns5:municipalityName>2</ns5:municipalityName>
\t\t\t\t\t<ns5:cantonAbbreviation>BE</ns5:cantonAbbreviation>
\t\t\t\t</ns1:municipality>
\t\t\t\t<ns1:buildingInformation>
\t\t\t\t\t<ns1:building>
\t\t\t\t\t\t<ns3:EGID>23</ns3:EGID>
\t\t\t\t\t\t<ns3:numberOfFloors>23</ns3:numberOfFloors>
\t\t\t\t\t\t<ns3:buildingCategory>1040</ns3:buildingCategory>
\t\t\t\t\t\t<ns3:civilDefenseShelter>true</ns3:civilDefenseShelter>
\t\t\t\t\t</ns1:building>
\t\t\t\t</ns1:buildingInformation>
\t\t\t\t<ns1:owner>
\t\t\t\t\t<ns1:ownerAdress>
\t\t\t\t\t\t<ns4:person>
\t\t\t\t\t\t\t<ns4:firstName>Winston</ns4:firstName>
\t\t\t\t\t\t\t<ns4:lastName>Smith</ns4:lastName>
\t\t\t\t\t\t</ns4:person>
\t\t\t\t\t\t<ns4:addressInformation>
\t\t\t\t\t\t\t<ns4:street>Teststrasse</ns4:street>
\t\t\t\t\t\t\t<ns4:houseNumber>23</ns4:houseNumber>
\t\t\t\t\t\t\t<ns4:town>Burgdorf</ns4:town>
\t\t\t\t\t\t\t<ns4:swissZipCode>2323</ns4:swissZipCode>
\t\t\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t\t\t</ns4:country>
\t\t\t\t\t\t</ns4:addressInformation>
\t\t\t\t\t</ns1:ownerAdress>
\t\t\t\t</ns1:owner>
\t\t\t</ns1:realestateInformation>
\t\t\t<ns1:zone>
\t\t\t\t<ns1:zoneDesignation>Testnutzungszone</ns1:zoneDesignation>
\t\t\t</ns1:zone>
\t\t\t<ns1:constructionProjectInformation>
\t\t\t\t<ns1:constructionProject>
\t\t\t\t\t<ns3:projectStartDate>2019-09-15</ns3:projectStartDate>
\t\t\t\t\t<ns3:totalCostsOfProject>232323</ns3:totalCostsOfProject>
\t\t\t\t\t<ns3:status>6701</ns3:status>
\t\t\t\t\t<ns3:description>Beschreibung&amp;#10;Mehr Beschreibung</ns3:description>
\t\t\t\t\t<ns3:durationOfConstructionPhase>23</ns3:durationOfConstructionPhase>
\t\t\t\t</ns1:constructionProject>
\t\t\t\t<ns1:municipality>
\t\t\t\t\t<ns5:municipalityName>2</ns5:municipalityName>
\t\t\t\t\t<ns5:cantonAbbreviation>BE</ns5:cantonAbbreviation>
\t\t\t\t</ns1:municipality>
\t\t\t</ns1:constructionProjectInformation>
\t\t\t<ns1:document>
\t\t\t\t<ns6:uuid>00000000-0000-0000-0000-000000000000</ns6:uuid>
\t\t\t\t<ns6:titles>
\t\t\t\t\t<ns7:title>dummy</ns7:title>
\t\t\t\t</ns6:titles>
\t\t\t\t<ns6:status>signed</ns6:status>
\t\t\t\t<ns6:files>
\t\t\t\t\t<ns6:file>
\t\t\t\t\t\t<ns6:pathFileName>unknown</ns6:pathFileName>
\t\t\t\t\t\t<ns6:mimeType>unknown</ns6:mimeType>
\t\t\t\t\t</ns6:file>
\t\t\t\t</ns6:files>
\t\t\t</ns1:document>
\t\t</ns1:planningPermissionApplication>
\t\t<ns1:relationshipToPerson>
\t\t\t<ns1:role>applicant</ns1:role>
\t\t\t<ns1:person>
\t\t\t\t<ns3:identification>
\t\t\t\t\t<ns3:personIdentification>
\t\t\t\t\t\t<ns8:officialName>Smith</ns8:officialName>
\t\t\t\t\t\t<ns8:firstName>Winston</ns8:firstName>
\t\t\t\t\t</ns3:personIdentification>
\t\t\t\t</ns3:identification>
\t\t\t\t<ns3:address>
\t\t\t\t\t<ns4:street>Teststrasse</ns4:street>
\t\t\t\t\t<ns4:houseNumber>23</ns4:houseNumber>
\t\t\t\t\t<ns4:town>Burgdorf</ns4:town>
\t\t\t\t\t<ns4:swissZipCode>2323</ns4:swissZipCode>
\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t</ns4:country>
\t\t\t\t</ns3:address>
\t\t\t</ns1:person>
\t\t</ns1:relationshipToPerson>
\t\t<ns1:relationshipToPerson>
\t\t\t<ns1:role>contact</ns1:role>
\t\t\t<ns1:person>
\t\t\t\t<ns3:identification>
\t\t\t\t\t<ns3:organisationIdentification>
\t\t\t\t\t\t<ns9:uid>
\t\t\t\t\t\t\t<ns9:uidOrganisationIdCategorie>CHE</ns9:uidOrganisationIdCategorie>
\t\t\t\t\t\t\t<ns9:uidOrganisationId>123123123</ns9:uidOrganisationId>
\t\t\t\t\t\t</ns9:uid>
\t\t\t\t\t\t<ns9:localOrganisationId>
\t\t\t\t\t\t\t<ns9:organisationIdCategory>unknown</ns9:organisationIdCategory>
\t\t\t\t\t\t\t<ns9:organisationId><!-- ORGANISATION_ID --></ns9:organisationId>
\t\t\t\t\t\t</ns9:localOrganisationId>
\t\t\t\t\t\t<ns9:organisationName>Firma XY AG</ns9:organisationName>
\t\t\t\t\t\t<ns9:organisationAdditionalName>Winston Smith</ns9:organisationAdditionalName>
\t\t\t\t\t\t<ns9:legalForm>0223</ns9:legalForm>
\t\t\t\t\t</ns3:organisationIdentification>
\t\t\t\t</ns3:identification>
\t\t\t\t<ns3:address>
\t\t\t\t\t<ns4:street>Teststrasse</ns4:street>
\t\t\t\t\t<ns4:houseNumber>23</ns4:houseNumber>
\t\t\t\t\t<ns4:town>Burgdorf</ns4:town>
\t\t\t\t\t<ns4:swissZipCode>2323</ns4:swissZipCode>
\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t</ns4:country>
\t\t\t\t</ns3:address>
\t\t\t</ns1:person>
\t\t</ns1:relationshipToPerson>
\t\t<ns1:relationshipToPerson>
\t\t\t<ns1:role>project author</ns1:role>
\t\t\t<ns1:person>
\t\t\t\t<ns3:identification>
\t\t\t\t\t<ns3:personIdentification>
\t\t\t\t\t\t<ns8:officialName>Smith</ns8:officialName>
\t\t\t\t\t\t<ns8:firstName>Winston</ns8:firstName>
\t\t\t\t\t</ns3:personIdentification>
\t\t\t\t</ns3:identification>
\t\t\t\t<ns3:address>
\t\t\t\t\t<ns4:street>Teststrasse</ns4:street>
\t\t\t\t\t<ns4:houseNumber>None</ns4:houseNumber>
\t\t\t\t\t<ns4:town>Burgdorf</ns4:town>
\t\t\t\t\t<ns4:swissZipCode>2323</ns4:swissZipCode>
\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t</ns4:country>
\t\t\t\t</ns3:address>
\t\t\t</ns1:person>
\t\t</ns1:relationshipToPerson>
\t\t<ns1:relationshipToPerson>
\t\t\t<ns1:role>landowner</ns1:role>
\t\t\t<ns1:person>
\t\t\t\t<ns3:identification>
\t\t\t\t\t<ns3:personIdentification>
\t\t\t\t\t\t<ns8:officialName>Smith</ns8:officialName>
\t\t\t\t\t\t<ns8:firstName>Winston</ns8:firstName>
\t\t\t\t\t</ns3:personIdentification>
\t\t\t\t</ns3:identification>
\t\t\t\t<ns3:address>
\t\t\t\t\t<ns4:street>Teststrasse</ns4:street>
\t\t\t\t\t<ns4:houseNumber>23</ns4:houseNumber>
\t\t\t\t\t<ns4:town>Burgdorf</ns4:town>
\t\t\t\t\t<ns4:swissZipCode>2323</ns4:swissZipCode>
\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t</ns4:country>
\t\t\t\t</ns3:address>
\t\t\t</ns1:person>
\t\t</ns1:relationshipToPerson>
\t</ns1:eventSubmitPlanningPermissionApplication>
</ns1:delivery>
'''

snapshots['test_event_handlers[StatusNotification] 1'] = '''<?xml version="1.0" ?>
<ns1:delivery xmlns:ns1="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0129/5">
\t<ns1:deliveryHeader>
\t\t<ns2:senderId>https://ebau.apps.be.ch/</ns2:senderId>
\t\t<ns2:messageId><!-- MESSAGE_ID --></ns2:messageId>
\t\t<ns2:messageType>5200030</ns2:messageType>
\t\t<ns2:sendingApplication>
\t\t\t<ns2:manufacturer>Adfinis AG</ns2:manufacturer>
\t\t\t<ns2:product>camac</ns2:product>
\t\t\t<ns2:productVersion><!-- VERSION --></ns2:productVersion>
\t\t</ns2:sendingApplication>
\t\t<ns2:subject>status notification</ns2:subject>
\t\t<ns2:messageDate>2022-06-03T00:00:00Z</ns2:messageDate>
\t\t<ns2:action>1</ns2:action>
\t\t<ns2:testDeliveryFlag>true</ns2:testDeliveryFlag>
\t</ns1:deliveryHeader>
\t<ns1:eventStatusNotification>
\t\t<ns1:eventType>status notification</ns1:eventType>
\t\t<ns1:planningPermissionApplicationIdentification>
\t\t\t<ns1:localID>
\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t<ns3:Id>unknown</ns3:Id>
\t\t\t</ns1:localID>
\t\t\t<ns1:otherID>
\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t<ns3:Id>unknown</ns3:Id>
\t\t\t</ns1:otherID>
\t\t\t<ns1:dossierIdentification><!-- INSTANCE_ID --></ns1:dossierIdentification>
\t\t</ns1:planningPermissionApplicationIdentification>
\t\t<ns1:status>in progress</ns1:status>
\t\t<ns1:remark>circulation_init</ns1:remark>
\t</ns1:eventStatusNotification>
</ns1:delivery>
'''

snapshots['test_event_handlers[WithdrawPlanningPermissionApplication] 1'] = '''<?xml version="1.0" ?>
<ns1:delivery xmlns:ns1="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0129/5">
\t<ns1:deliveryHeader>
\t\t<ns2:senderId>https://ebau.apps.be.ch/</ns2:senderId>
\t\t<ns2:messageId><!-- MESSAGE_ID --></ns2:messageId>
\t\t<ns2:messageType>5100002</ns2:messageType>
\t\t<ns2:sendingApplication>
\t\t\t<ns2:manufacturer>Adfinis AG</ns2:manufacturer>
\t\t\t<ns2:product>camac</ns2:product>
\t\t\t<ns2:productVersion><!-- VERSION --></ns2:productVersion>
\t\t</ns2:sendingApplication>
\t\t<ns2:subject>withdraw planning permission application</ns2:subject>
\t\t<ns2:messageDate>2022-06-03T00:00:00Z</ns2:messageDate>
\t\t<ns2:action>1</ns2:action>
\t\t<ns2:testDeliveryFlag>true</ns2:testDeliveryFlag>
\t</ns1:deliveryHeader>
\t<ns1:eventRequest>
\t\t<ns1:eventType>withdraw planning permission application</ns1:eventType>
\t\t<ns1:planningPermissionApplicationIdentification>
\t\t\t<ns1:localID>
\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t<ns3:Id>unknown</ns3:Id>
\t\t\t</ns1:localID>
\t\t\t<ns1:otherID>
\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t<ns3:Id>unknown</ns3:Id>
\t\t\t</ns1:otherID>
\t\t\t<ns1:dossierIdentification><!-- INSTANCE_ID --></ns1:dossierIdentification>
\t\t</ns1:planningPermissionApplicationIdentification>
\t</ns1:eventRequest>
</ns1:delivery>
'''

snapshots['test_file_subsequently_signal 1'] = '''<?xml version="1.0" ?>
<ns1:delivery xmlns:ns1="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0129/5" xmlns:ns4="http://www.ech.ch/xmlns/eCH-0010/6" xmlns:ns5="http://www.ech.ch/xmlns/eCH-0007/6" xmlns:ns6="http://www.ech.ch/xmlns/eCH-0147/T0/1" xmlns:ns7="http://www.ech.ch/xmlns/eCH-0039/2" xmlns:ns8="http://www.ech.ch/xmlns/eCH-0044/4" xmlns:ns9="http://www.ech.ch/xmlns/eCH-0097/2">
\t<ns1:deliveryHeader>
\t\t<ns2:senderId>https://ebau.apps.be.ch/</ns2:senderId>
\t\t<ns2:messageId><!-- MESSAGE_ID --></ns2:messageId>
\t\t<ns2:messageType>5100001</ns2:messageType>
\t\t<ns2:sendingApplication>
\t\t\t<ns2:manufacturer>Adfinis AG</ns2:manufacturer>
\t\t\t<ns2:product>camac</ns2:product>
\t\t\t<ns2:productVersion><!-- VERSION --></ns2:productVersion>
\t\t</ns2:sendingApplication>
\t\t<ns2:subject>Generelles Baugesuch</ns2:subject>
\t\t<ns2:messageDate>2022-06-03T00:00:00Z</ns2:messageDate>
\t\t<ns2:action>1</ns2:action>
\t\t<ns2:testDeliveryFlag>true</ns2:testDeliveryFlag>
\t</ns1:deliveryHeader>
\t<ns1:eventSubmitPlanningPermissionApplication>
\t\t<ns1:eventType>file subsequently</ns1:eventType>
\t\t<ns1:planningPermissionApplication>
\t\t\t<ns1:planningPermissionApplicationIdentification>
\t\t\t\t<ns1:localID>
\t\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t\t<ns3:Id>2020-1</ns3:Id>
\t\t\t\t</ns1:localID>
\t\t\t\t<ns1:otherID>
\t\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t\t<ns3:Id>2020-1</ns3:Id>
\t\t\t\t</ns1:otherID>
\t\t\t\t<ns1:dossierIdentification><!-- INSTANCE_ID --></ns1:dossierIdentification>
\t\t\t</ns1:planningPermissionApplicationIdentification>
\t\t\t<ns1:description>Beschreibung&amp;#10;Mehr Beschreibung</ns1:description>
\t\t\t<ns1:applicationType>Generelles Baugesuch</ns1:applicationType>
\t\t\t<ns1:remark>Foo bar</ns1:remark>
\t\t\t<ns1:intendedPurpose>Wohnen</ns1:intendedPurpose>
\t\t\t<ns1:parkingLotsYesNo>true</ns1:parkingLotsYesNo>
\t\t\t<ns1:natureRisk>
\t\t\t\t<ns1:riskDesignation>Fliesslawine</ns1:riskDesignation>
\t\t\t\t<ns1:riskExists>true</ns1:riskExists>
\t\t\t</ns1:natureRisk>
\t\t\t<ns1:constructionCost>232323.0</ns1:constructionCost>
\t\t\t<ns1:namedMetaData>
\t\t\t\t<ns3:metaDataName>status</ns3:metaDataName>
\t\t\t\t<ns3:metaDataValue>David Rangel</ns3:metaDataValue>
\t\t\t</ns1:namedMetaData>
\t\t\t<ns1:locationAddress>
\t\t\t\t<ns4:street>Teststrasse</ns4:street>
\t\t\t\t<ns4:houseNumber>23</ns4:houseNumber>
\t\t\t\t<ns4:town>Burgdorf</ns4:town>
\t\t\t\t<ns4:swissZipCode>9999</ns4:swissZipCode>
\t\t\t\t<ns4:country>
\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t</ns4:country>
\t\t\t</ns1:locationAddress>
\t\t\t<ns1:realestateInformation>
\t\t\t\t<ns1:realestate>
\t\t\t\t\t<ns3:realestateIdentification>
\t\t\t\t\t\t<ns3:EGRID>23</ns3:EGRID>
\t\t\t\t\t\t<ns3:number>1586</ns3:number>
\t\t\t\t\t</ns3:realestateIdentification>
\t\t\t\t\t<ns3:realestateType>8</ns3:realestateType>
\t\t\t\t\t<ns3:coordinates>
\t\t\t\t\t\t<ns3:LV95>
\t\t\t\t\t\t\t<ns3:east>2480034.0</ns3:east>
\t\t\t\t\t\t\t<ns3:north>1070500.0</ns3:north>
\t\t\t\t\t\t\t<ns3:originOfCoordinates>904</ns3:originOfCoordinates>
\t\t\t\t\t\t</ns3:LV95>
\t\t\t\t\t</ns3:coordinates>
\t\t\t\t</ns1:realestate>
\t\t\t\t<ns1:municipality>
\t\t\t\t\t<ns5:municipalityName>2</ns5:municipalityName>
\t\t\t\t\t<ns5:cantonAbbreviation>BE</ns5:cantonAbbreviation>
\t\t\t\t</ns1:municipality>
\t\t\t\t<ns1:buildingInformation>
\t\t\t\t\t<ns1:building>
\t\t\t\t\t\t<ns3:EGID>23</ns3:EGID>
\t\t\t\t\t\t<ns3:numberOfFloors>23</ns3:numberOfFloors>
\t\t\t\t\t\t<ns3:buildingCategory>1040</ns3:buildingCategory>
\t\t\t\t\t\t<ns3:civilDefenseShelter>true</ns3:civilDefenseShelter>
\t\t\t\t\t</ns1:building>
\t\t\t\t</ns1:buildingInformation>
\t\t\t\t<ns1:owner>
\t\t\t\t\t<ns1:ownerAdress>
\t\t\t\t\t\t<ns4:person>
\t\t\t\t\t\t\t<ns4:firstName>Winston</ns4:firstName>
\t\t\t\t\t\t\t<ns4:lastName>Smith</ns4:lastName>
\t\t\t\t\t\t</ns4:person>
\t\t\t\t\t\t<ns4:addressInformation>
\t\t\t\t\t\t\t<ns4:street>Teststrasse</ns4:street>
\t\t\t\t\t\t\t<ns4:houseNumber>23</ns4:houseNumber>
\t\t\t\t\t\t\t<ns4:town>Burgdorf</ns4:town>
\t\t\t\t\t\t\t<ns4:swissZipCode>2323</ns4:swissZipCode>
\t\t\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t\t\t</ns4:country>
\t\t\t\t\t\t</ns4:addressInformation>
\t\t\t\t\t</ns1:ownerAdress>
\t\t\t\t</ns1:owner>
\t\t\t</ns1:realestateInformation>
\t\t\t<ns1:realestateInformation>
\t\t\t\t<ns1:realestate>
\t\t\t\t\t<ns3:realestateIdentification>
\t\t\t\t\t\t<ns3:EGRID>24</ns3:EGRID>
\t\t\t\t\t\t<ns3:number>1587</ns3:number>
\t\t\t\t\t</ns3:realestateIdentification>
\t\t\t\t\t<ns3:realestateType>8</ns3:realestateType>
\t\t\t\t\t<ns3:coordinates>
\t\t\t\t\t\t<ns3:LV95>
\t\t\t\t\t\t\t<ns3:east>2480035.0</ns3:east>
\t\t\t\t\t\t\t<ns3:north>1070600.0</ns3:north>
\t\t\t\t\t\t\t<ns3:originOfCoordinates>904</ns3:originOfCoordinates>
\t\t\t\t\t\t</ns3:LV95>
\t\t\t\t\t</ns3:coordinates>
\t\t\t\t</ns1:realestate>
\t\t\t\t<ns1:municipality>
\t\t\t\t\t<ns5:municipalityName>2</ns5:municipalityName>
\t\t\t\t\t<ns5:cantonAbbreviation>BE</ns5:cantonAbbreviation>
\t\t\t\t</ns1:municipality>
\t\t\t\t<ns1:buildingInformation>
\t\t\t\t\t<ns1:building>
\t\t\t\t\t\t<ns3:EGID>23</ns3:EGID>
\t\t\t\t\t\t<ns3:numberOfFloors>23</ns3:numberOfFloors>
\t\t\t\t\t\t<ns3:buildingCategory>1040</ns3:buildingCategory>
\t\t\t\t\t\t<ns3:civilDefenseShelter>true</ns3:civilDefenseShelter>
\t\t\t\t\t</ns1:building>
\t\t\t\t</ns1:buildingInformation>
\t\t\t\t<ns1:owner>
\t\t\t\t\t<ns1:ownerAdress>
\t\t\t\t\t\t<ns4:person>
\t\t\t\t\t\t\t<ns4:firstName>Winston</ns4:firstName>
\t\t\t\t\t\t\t<ns4:lastName>Smith</ns4:lastName>
\t\t\t\t\t\t</ns4:person>
\t\t\t\t\t\t<ns4:addressInformation>
\t\t\t\t\t\t\t<ns4:street>Teststrasse</ns4:street>
\t\t\t\t\t\t\t<ns4:houseNumber>23</ns4:houseNumber>
\t\t\t\t\t\t\t<ns4:town>Burgdorf</ns4:town>
\t\t\t\t\t\t\t<ns4:swissZipCode>2323</ns4:swissZipCode>
\t\t\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t\t\t</ns4:country>
\t\t\t\t\t\t</ns4:addressInformation>
\t\t\t\t\t</ns1:ownerAdress>
\t\t\t\t</ns1:owner>
\t\t\t</ns1:realestateInformation>
\t\t\t<ns1:zone>
\t\t\t\t<ns1:zoneDesignation>Testnutzungszone</ns1:zoneDesignation>
\t\t\t</ns1:zone>
\t\t\t<ns1:constructionProjectInformation>
\t\t\t\t<ns1:constructionProject>
\t\t\t\t\t<ns3:projectStartDate>2019-09-15</ns3:projectStartDate>
\t\t\t\t\t<ns3:totalCostsOfProject>232323</ns3:totalCostsOfProject>
\t\t\t\t\t<ns3:status>6701</ns3:status>
\t\t\t\t\t<ns3:description>Beschreibung&amp;#10;Mehr Beschreibung</ns3:description>
\t\t\t\t\t<ns3:durationOfConstructionPhase>23</ns3:durationOfConstructionPhase>
\t\t\t\t</ns1:constructionProject>
\t\t\t\t<ns1:municipality>
\t\t\t\t\t<ns5:municipalityName>2</ns5:municipalityName>
\t\t\t\t\t<ns5:cantonAbbreviation>BE</ns5:cantonAbbreviation>
\t\t\t\t</ns1:municipality>
\t\t\t</ns1:constructionProjectInformation>
\t\t\t<ns1:document>
\t\t\t\t<ns6:uuid>00000000-0000-0000-0000-000000000000</ns6:uuid>
\t\t\t\t<ns6:titles>
\t\t\t\t\t<ns7:title>dummy</ns7:title>
\t\t\t\t</ns6:titles>
\t\t\t\t<ns6:status>signed</ns6:status>
\t\t\t\t<ns6:files>
\t\t\t\t\t<ns6:file>
\t\t\t\t\t\t<ns6:pathFileName>unknown</ns6:pathFileName>
\t\t\t\t\t\t<ns6:mimeType>unknown</ns6:mimeType>
\t\t\t\t\t</ns6:file>
\t\t\t\t</ns6:files>
\t\t\t</ns1:document>
\t\t</ns1:planningPermissionApplication>
\t\t<ns1:relationshipToPerson>
\t\t\t<ns1:role>applicant</ns1:role>
\t\t\t<ns1:person>
\t\t\t\t<ns3:identification>
\t\t\t\t\t<ns3:personIdentification>
\t\t\t\t\t\t<ns8:officialName>Smith</ns8:officialName>
\t\t\t\t\t\t<ns8:firstName>Winston</ns8:firstName>
\t\t\t\t\t</ns3:personIdentification>
\t\t\t\t</ns3:identification>
\t\t\t\t<ns3:address>
\t\t\t\t\t<ns4:street>Teststrasse</ns4:street>
\t\t\t\t\t<ns4:houseNumber>23</ns4:houseNumber>
\t\t\t\t\t<ns4:town>Burgdorf</ns4:town>
\t\t\t\t\t<ns4:swissZipCode>2323</ns4:swissZipCode>
\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t</ns4:country>
\t\t\t\t</ns3:address>
\t\t\t</ns1:person>
\t\t</ns1:relationshipToPerson>
\t\t<ns1:relationshipToPerson>
\t\t\t<ns1:role>contact</ns1:role>
\t\t\t<ns1:person>
\t\t\t\t<ns3:identification>
\t\t\t\t\t<ns3:organisationIdentification>
\t\t\t\t\t\t<ns9:uid>
\t\t\t\t\t\t\t<ns9:uidOrganisationIdCategorie>CHE</ns9:uidOrganisationIdCategorie>
\t\t\t\t\t\t\t<ns9:uidOrganisationId>123123123</ns9:uidOrganisationId>
\t\t\t\t\t\t</ns9:uid>
\t\t\t\t\t\t<ns9:localOrganisationId>
\t\t\t\t\t\t\t<ns9:organisationIdCategory>unknown</ns9:organisationIdCategory>
\t\t\t\t\t\t\t<ns9:organisationId><!-- ORGANISATION_ID --></ns9:organisationId>
\t\t\t\t\t\t</ns9:localOrganisationId>
\t\t\t\t\t\t<ns9:organisationName>Firma XY AG</ns9:organisationName>
\t\t\t\t\t\t<ns9:organisationAdditionalName>Winston Smith</ns9:organisationAdditionalName>
\t\t\t\t\t\t<ns9:legalForm>0223</ns9:legalForm>
\t\t\t\t\t</ns3:organisationIdentification>
\t\t\t\t</ns3:identification>
\t\t\t\t<ns3:address>
\t\t\t\t\t<ns4:street>Teststrasse</ns4:street>
\t\t\t\t\t<ns4:houseNumber>23</ns4:houseNumber>
\t\t\t\t\t<ns4:town>Burgdorf</ns4:town>
\t\t\t\t\t<ns4:swissZipCode>2323</ns4:swissZipCode>
\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t</ns4:country>
\t\t\t\t</ns3:address>
\t\t\t</ns1:person>
\t\t</ns1:relationshipToPerson>
\t\t<ns1:relationshipToPerson>
\t\t\t<ns1:role>project author</ns1:role>
\t\t\t<ns1:person>
\t\t\t\t<ns3:identification>
\t\t\t\t\t<ns3:personIdentification>
\t\t\t\t\t\t<ns8:officialName>Smith</ns8:officialName>
\t\t\t\t\t\t<ns8:firstName>Winston</ns8:firstName>
\t\t\t\t\t</ns3:personIdentification>
\t\t\t\t</ns3:identification>
\t\t\t\t<ns3:address>
\t\t\t\t\t<ns4:street>Teststrasse</ns4:street>
\t\t\t\t\t<ns4:houseNumber>None</ns4:houseNumber>
\t\t\t\t\t<ns4:town>Burgdorf</ns4:town>
\t\t\t\t\t<ns4:swissZipCode>2323</ns4:swissZipCode>
\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t</ns4:country>
\t\t\t\t</ns3:address>
\t\t\t</ns1:person>
\t\t</ns1:relationshipToPerson>
\t\t<ns1:relationshipToPerson>
\t\t\t<ns1:role>landowner</ns1:role>
\t\t\t<ns1:person>
\t\t\t\t<ns3:identification>
\t\t\t\t\t<ns3:personIdentification>
\t\t\t\t\t\t<ns8:officialName>Smith</ns8:officialName>
\t\t\t\t\t\t<ns8:firstName>Winston</ns8:firstName>
\t\t\t\t\t</ns3:personIdentification>
\t\t\t\t</ns3:identification>
\t\t\t\t<ns3:address>
\t\t\t\t\t<ns4:street>Teststrasse</ns4:street>
\t\t\t\t\t<ns4:houseNumber>23</ns4:houseNumber>
\t\t\t\t\t<ns4:town>Burgdorf</ns4:town>
\t\t\t\t\t<ns4:swissZipCode>2323</ns4:swissZipCode>
\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t</ns4:country>
\t\t\t\t</ns3:address>
\t\t\t</ns1:person>
\t\t</ns1:relationshipToPerson>
\t</ns1:eventSubmitPlanningPermissionApplication>
</ns1:delivery>
'''

snapshots['test_submit_event[True] 1'] = '''<?xml version="1.0" ?>
<ns1:delivery xmlns:ns1="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0129/5" xmlns:ns4="http://www.ech.ch/xmlns/eCH-0010/6" xmlns:ns5="http://www.ech.ch/xmlns/eCH-0007/6" xmlns:ns6="http://www.ech.ch/xmlns/eCH-0147/T0/1" xmlns:ns7="http://www.ech.ch/xmlns/eCH-0039/2" xmlns:ns8="http://www.ech.ch/xmlns/eCH-0044/4" xmlns:ns9="http://www.ech.ch/xmlns/eCH-0097/2">
\t<ns1:deliveryHeader>
\t\t<ns2:senderId>https://ebau.apps.be.ch/</ns2:senderId>
\t\t<ns2:messageId><!-- MESSAGE_ID --></ns2:messageId>
\t\t<ns2:messageType>5100000</ns2:messageType>
\t\t<ns2:sendingApplication>
\t\t\t<ns2:manufacturer>Adfinis AG</ns2:manufacturer>
\t\t\t<ns2:product>camac</ns2:product>
\t\t\t<ns2:productVersion><!-- VERSION --></ns2:productVersion>
\t\t</ns2:sendingApplication>
\t\t<ns2:subject>Generelles Baugesuch</ns2:subject>
\t\t<ns2:messageDate>2022-06-03T00:00:00Z</ns2:messageDate>
\t\t<ns2:action>1</ns2:action>
\t\t<ns2:testDeliveryFlag>true</ns2:testDeliveryFlag>
\t</ns1:deliveryHeader>
\t<ns1:eventSubmitPlanningPermissionApplication>
\t\t<ns1:eventType>submit</ns1:eventType>
\t\t<ns1:planningPermissionApplication>
\t\t\t<ns1:planningPermissionApplicationIdentification>
\t\t\t\t<ns1:localID>
\t\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t\t<ns3:Id>2020-1</ns3:Id>
\t\t\t\t</ns1:localID>
\t\t\t\t<ns1:otherID>
\t\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t\t<ns3:Id>2020-1</ns3:Id>
\t\t\t\t</ns1:otherID>
\t\t\t\t<ns1:dossierIdentification><!-- INSTANCE_ID --></ns1:dossierIdentification>
\t\t\t</ns1:planningPermissionApplicationIdentification>
\t\t\t<ns1:description>Beschreibung&amp;#10;Mehr Beschreibung</ns1:description>
\t\t\t<ns1:applicationType>Generelles Baugesuch</ns1:applicationType>
\t\t\t<ns1:remark>Foo bar</ns1:remark>
\t\t\t<ns1:intendedPurpose>Wohnen</ns1:intendedPurpose>
\t\t\t<ns1:parkingLotsYesNo>true</ns1:parkingLotsYesNo>
\t\t\t<ns1:natureRisk>
\t\t\t\t<ns1:riskDesignation>Fliesslawine</ns1:riskDesignation>
\t\t\t\t<ns1:riskExists>true</ns1:riskExists>
\t\t\t</ns1:natureRisk>
\t\t\t<ns1:constructionCost>232323.0</ns1:constructionCost>
\t\t\t<ns1:namedMetaData>
\t\t\t\t<ns3:metaDataName>status</ns3:metaDataName>
\t\t\t\t<ns3:metaDataValue>David Rangel</ns3:metaDataValue>
\t\t\t</ns1:namedMetaData>
\t\t\t<ns1:locationAddress>
\t\t\t\t<ns4:street>Teststrasse</ns4:street>
\t\t\t\t<ns4:houseNumber>23</ns4:houseNumber>
\t\t\t\t<ns4:town>Burgdorf</ns4:town>
\t\t\t\t<ns4:swissZipCode>9999</ns4:swissZipCode>
\t\t\t\t<ns4:country>
\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t</ns4:country>
\t\t\t</ns1:locationAddress>
\t\t\t<ns1:realestateInformation>
\t\t\t\t<ns1:realestate>
\t\t\t\t\t<ns3:realestateIdentification>
\t\t\t\t\t\t<ns3:EGRID>23</ns3:EGRID>
\t\t\t\t\t\t<ns3:number>1586</ns3:number>
\t\t\t\t\t</ns3:realestateIdentification>
\t\t\t\t\t<ns3:realestateType>8</ns3:realestateType>
\t\t\t\t\t<ns3:coordinates>
\t\t\t\t\t\t<ns3:LV95>
\t\t\t\t\t\t\t<ns3:east>2480034.0</ns3:east>
\t\t\t\t\t\t\t<ns3:north>1070500.0</ns3:north>
\t\t\t\t\t\t\t<ns3:originOfCoordinates>904</ns3:originOfCoordinates>
\t\t\t\t\t\t</ns3:LV95>
\t\t\t\t\t</ns3:coordinates>
\t\t\t\t</ns1:realestate>
\t\t\t\t<ns1:municipality>
\t\t\t\t\t<ns5:municipalityName>2</ns5:municipalityName>
\t\t\t\t\t<ns5:cantonAbbreviation>BE</ns5:cantonAbbreviation>
\t\t\t\t</ns1:municipality>
\t\t\t\t<ns1:buildingInformation>
\t\t\t\t\t<ns1:building>
\t\t\t\t\t\t<ns3:EGID>23</ns3:EGID>
\t\t\t\t\t\t<ns3:numberOfFloors>23</ns3:numberOfFloors>
\t\t\t\t\t\t<ns3:buildingCategory>1040</ns3:buildingCategory>
\t\t\t\t\t\t<ns3:civilDefenseShelter>true</ns3:civilDefenseShelter>
\t\t\t\t\t</ns1:building>
\t\t\t\t</ns1:buildingInformation>
\t\t\t\t<ns1:owner>
\t\t\t\t\t<ns1:ownerAdress>
\t\t\t\t\t\t<ns4:person>
\t\t\t\t\t\t\t<ns4:firstName>Winston</ns4:firstName>
\t\t\t\t\t\t\t<ns4:lastName>Smith</ns4:lastName>
\t\t\t\t\t\t</ns4:person>
\t\t\t\t\t\t<ns4:addressInformation>
\t\t\t\t\t\t\t<ns4:street>Teststrasse</ns4:street>
\t\t\t\t\t\t\t<ns4:houseNumber>23</ns4:houseNumber>
\t\t\t\t\t\t\t<ns4:town>Burgdorf</ns4:town>
\t\t\t\t\t\t\t<ns4:swissZipCode>2323</ns4:swissZipCode>
\t\t\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t\t\t</ns4:country>
\t\t\t\t\t\t</ns4:addressInformation>
\t\t\t\t\t</ns1:ownerAdress>
\t\t\t\t</ns1:owner>
\t\t\t</ns1:realestateInformation>
\t\t\t<ns1:realestateInformation>
\t\t\t\t<ns1:realestate>
\t\t\t\t\t<ns3:realestateIdentification>
\t\t\t\t\t\t<ns3:EGRID>24</ns3:EGRID>
\t\t\t\t\t\t<ns3:number>1587</ns3:number>
\t\t\t\t\t</ns3:realestateIdentification>
\t\t\t\t\t<ns3:realestateType>8</ns3:realestateType>
\t\t\t\t\t<ns3:coordinates>
\t\t\t\t\t\t<ns3:LV95>
\t\t\t\t\t\t\t<ns3:east>2480035.0</ns3:east>
\t\t\t\t\t\t\t<ns3:north>1070600.0</ns3:north>
\t\t\t\t\t\t\t<ns3:originOfCoordinates>904</ns3:originOfCoordinates>
\t\t\t\t\t\t</ns3:LV95>
\t\t\t\t\t</ns3:coordinates>
\t\t\t\t</ns1:realestate>
\t\t\t\t<ns1:municipality>
\t\t\t\t\t<ns5:municipalityName>2</ns5:municipalityName>
\t\t\t\t\t<ns5:cantonAbbreviation>BE</ns5:cantonAbbreviation>
\t\t\t\t</ns1:municipality>
\t\t\t\t<ns1:buildingInformation>
\t\t\t\t\t<ns1:building>
\t\t\t\t\t\t<ns3:EGID>23</ns3:EGID>
\t\t\t\t\t\t<ns3:numberOfFloors>23</ns3:numberOfFloors>
\t\t\t\t\t\t<ns3:buildingCategory>1040</ns3:buildingCategory>
\t\t\t\t\t\t<ns3:civilDefenseShelter>true</ns3:civilDefenseShelter>
\t\t\t\t\t</ns1:building>
\t\t\t\t</ns1:buildingInformation>
\t\t\t\t<ns1:owner>
\t\t\t\t\t<ns1:ownerAdress>
\t\t\t\t\t\t<ns4:person>
\t\t\t\t\t\t\t<ns4:firstName>Winston</ns4:firstName>
\t\t\t\t\t\t\t<ns4:lastName>Smith</ns4:lastName>
\t\t\t\t\t\t</ns4:person>
\t\t\t\t\t\t<ns4:addressInformation>
\t\t\t\t\t\t\t<ns4:street>Teststrasse</ns4:street>
\t\t\t\t\t\t\t<ns4:houseNumber>23</ns4:houseNumber>
\t\t\t\t\t\t\t<ns4:town>Burgdorf</ns4:town>
\t\t\t\t\t\t\t<ns4:swissZipCode>2323</ns4:swissZipCode>
\t\t\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t\t\t</ns4:country>
\t\t\t\t\t\t</ns4:addressInformation>
\t\t\t\t\t</ns1:ownerAdress>
\t\t\t\t</ns1:owner>
\t\t\t</ns1:realestateInformation>
\t\t\t<ns1:zone>
\t\t\t\t<ns1:zoneDesignation>Testnutzungszone</ns1:zoneDesignation>
\t\t\t</ns1:zone>
\t\t\t<ns1:constructionProjectInformation>
\t\t\t\t<ns1:constructionProject>
\t\t\t\t\t<ns3:projectStartDate>2019-09-15</ns3:projectStartDate>
\t\t\t\t\t<ns3:totalCostsOfProject>232323</ns3:totalCostsOfProject>
\t\t\t\t\t<ns3:status>6701</ns3:status>
\t\t\t\t\t<ns3:description>Beschreibung&amp;#10;Mehr Beschreibung</ns3:description>
\t\t\t\t\t<ns3:durationOfConstructionPhase>23</ns3:durationOfConstructionPhase>
\t\t\t\t</ns1:constructionProject>
\t\t\t\t<ns1:municipality>
\t\t\t\t\t<ns5:municipalityName>2</ns5:municipalityName>
\t\t\t\t\t<ns5:cantonAbbreviation>BE</ns5:cantonAbbreviation>
\t\t\t\t</ns1:municipality>
\t\t\t</ns1:constructionProjectInformation>
\t\t\t<ns1:document>
\t\t\t\t<ns6:uuid>00000000-0000-0000-0000-000000000000</ns6:uuid>
\t\t\t\t<ns6:titles>
\t\t\t\t\t<ns7:title>dummy</ns7:title>
\t\t\t\t</ns6:titles>
\t\t\t\t<ns6:status>signed</ns6:status>
\t\t\t\t<ns6:files>
\t\t\t\t\t<ns6:file>
\t\t\t\t\t\t<ns6:pathFileName>unknown</ns6:pathFileName>
\t\t\t\t\t\t<ns6:mimeType>unknown</ns6:mimeType>
\t\t\t\t\t</ns6:file>
\t\t\t\t</ns6:files>
\t\t\t</ns1:document>
\t\t</ns1:planningPermissionApplication>
\t\t<ns1:relationshipToPerson>
\t\t\t<ns1:role>applicant</ns1:role>
\t\t\t<ns1:person>
\t\t\t\t<ns3:identification>
\t\t\t\t\t<ns3:personIdentification>
\t\t\t\t\t\t<ns8:officialName>Smith</ns8:officialName>
\t\t\t\t\t\t<ns8:firstName>Winston</ns8:firstName>
\t\t\t\t\t</ns3:personIdentification>
\t\t\t\t</ns3:identification>
\t\t\t\t<ns3:address>
\t\t\t\t\t<ns4:street>Teststrasse</ns4:street>
\t\t\t\t\t<ns4:houseNumber>23</ns4:houseNumber>
\t\t\t\t\t<ns4:town>Burgdorf</ns4:town>
\t\t\t\t\t<ns4:swissZipCode>2323</ns4:swissZipCode>
\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t</ns4:country>
\t\t\t\t</ns3:address>
\t\t\t</ns1:person>
\t\t</ns1:relationshipToPerson>
\t\t<ns1:relationshipToPerson>
\t\t\t<ns1:role>contact</ns1:role>
\t\t\t<ns1:person>
\t\t\t\t<ns3:identification>
\t\t\t\t\t<ns3:organisationIdentification>
\t\t\t\t\t\t<ns9:uid>
\t\t\t\t\t\t\t<ns9:uidOrganisationIdCategorie>CHE</ns9:uidOrganisationIdCategorie>
\t\t\t\t\t\t\t<ns9:uidOrganisationId>123123123</ns9:uidOrganisationId>
\t\t\t\t\t\t</ns9:uid>
\t\t\t\t\t\t<ns9:localOrganisationId>
\t\t\t\t\t\t\t<ns9:organisationIdCategory>unknown</ns9:organisationIdCategory>
\t\t\t\t\t\t\t<ns9:organisationId><!-- ORGANISATION_ID --></ns9:organisationId>
\t\t\t\t\t\t</ns9:localOrganisationId>
\t\t\t\t\t\t<ns9:organisationName>Firma XY AG</ns9:organisationName>
\t\t\t\t\t\t<ns9:organisationAdditionalName>Winston Smith</ns9:organisationAdditionalName>
\t\t\t\t\t\t<ns9:legalForm>0223</ns9:legalForm>
\t\t\t\t\t</ns3:organisationIdentification>
\t\t\t\t</ns3:identification>
\t\t\t\t<ns3:address>
\t\t\t\t\t<ns4:street>Teststrasse</ns4:street>
\t\t\t\t\t<ns4:houseNumber>23</ns4:houseNumber>
\t\t\t\t\t<ns4:town>Burgdorf</ns4:town>
\t\t\t\t\t<ns4:swissZipCode>2323</ns4:swissZipCode>
\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t</ns4:country>
\t\t\t\t</ns3:address>
\t\t\t</ns1:person>
\t\t</ns1:relationshipToPerson>
\t\t<ns1:relationshipToPerson>
\t\t\t<ns1:role>project author</ns1:role>
\t\t\t<ns1:person>
\t\t\t\t<ns3:identification>
\t\t\t\t\t<ns3:personIdentification>
\t\t\t\t\t\t<ns8:officialName>Smith</ns8:officialName>
\t\t\t\t\t\t<ns8:firstName>Winston</ns8:firstName>
\t\t\t\t\t</ns3:personIdentification>
\t\t\t\t</ns3:identification>
\t\t\t\t<ns3:address>
\t\t\t\t\t<ns4:street>Teststrasse</ns4:street>
\t\t\t\t\t<ns4:houseNumber>None</ns4:houseNumber>
\t\t\t\t\t<ns4:town>Burgdorf</ns4:town>
\t\t\t\t\t<ns4:swissZipCode>2323</ns4:swissZipCode>
\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t</ns4:country>
\t\t\t\t</ns3:address>
\t\t\t</ns1:person>
\t\t</ns1:relationshipToPerson>
\t\t<ns1:relationshipToPerson>
\t\t\t<ns1:role>landowner</ns1:role>
\t\t\t<ns1:person>
\t\t\t\t<ns3:identification>
\t\t\t\t\t<ns3:personIdentification>
\t\t\t\t\t\t<ns8:officialName>Smith</ns8:officialName>
\t\t\t\t\t\t<ns8:firstName>Winston</ns8:firstName>
\t\t\t\t\t</ns3:personIdentification>
\t\t\t\t</ns3:identification>
\t\t\t\t<ns3:address>
\t\t\t\t\t<ns4:street>Teststrasse</ns4:street>
\t\t\t\t\t<ns4:houseNumber>23</ns4:houseNumber>
\t\t\t\t\t<ns4:town>Burgdorf</ns4:town>
\t\t\t\t\t<ns4:swissZipCode>2323</ns4:swissZipCode>
\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t</ns4:country>
\t\t\t\t</ns3:address>
\t\t\t</ns1:person>
\t\t</ns1:relationshipToPerson>
\t</ns1:eventSubmitPlanningPermissionApplication>
</ns1:delivery>
'''

snapshots['test_submit_event_sz[basic-Support-instance__location0-baugesuch-instance__user0-1311-new] 1'] = '''<?xml version="1.0" ?>
<ns1:delivery xmlns:ns1="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0129/5" xmlns:ns4="http://www.ech.ch/xmlns/eCH-0010/6" xmlns:ns5="http://www.ech.ch/xmlns/eCH-0007/6" xmlns:ns6="http://www.ech.ch/xmlns/eCH-0147/T0/1" xmlns:ns7="http://www.ech.ch/xmlns/eCH-0039/2" xmlns:ns8="http://www.ech.ch/xmlns/eCH-0097/2" xmlns:ns9="http://www.ech.ch/xmlns/eCH-0044/4">
\t<ns1:deliveryHeader>
\t\t<ns2:senderId>https://behoerden.ebau-sz.ch/</ns2:senderId>
\t\t<ns2:messageId><!-- MESSAGE_ID --></ns2:messageId>
\t\t<ns2:messageType>5100000</ns2:messageType>
\t\t<ns2:sendingApplication>
\t\t\t<ns2:manufacturer>Adfinis AG</ns2:manufacturer>
\t\t\t<ns2:product>camac</ns2:product>
\t\t\t<ns2:productVersion><!-- VERSION --></ns2:productVersion>
\t\t</ns2:sendingApplication>
\t\t<ns2:subject>application_type</ns2:subject>
\t\t<ns2:messageDate>2022-07-07T00:00:00Z</ns2:messageDate>
\t\t<ns2:action>1</ns2:action>
\t\t<ns2:testDeliveryFlag>true</ns2:testDeliveryFlag>
\t</ns1:deliveryHeader>
\t<ns1:eventSubmitPlanningPermissionApplication>
\t\t<ns1:eventType>submit</ns1:eventType>
\t\t<ns1:planningPermissionApplication>
\t\t\t<ns1:planningPermissionApplicationIdentification>
\t\t\t\t<ns1:localID>
\t\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t\t<ns3:Id>TEST-90-22-001</ns3:Id>
\t\t\t\t</ns1:localID>
\t\t\t\t<ns1:otherID>
\t\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t\t<ns3:Id>TEST-90-22-001</ns3:Id>
\t\t\t\t</ns1:otherID>
\t\t\t\t<ns1:dossierIdentification><!-- INSTANCE_ID --></ns1:dossierIdentification>
\t\t\t</ns1:planningPermissionApplicationIdentification>
\t\t\t<ns1:description>None</ns1:description>
\t\t\t<ns1:applicationType>Brian Vasquez</ns1:applicationType>
\t\t\t<ns1:remark>None</ns1:remark>
\t\t\t<ns1:profilingYesNo>false</ns1:profilingYesNo>
\t\t\t<ns1:intendedPurpose>None</ns1:intendedPurpose>
\t\t\t<ns1:namedMetaData>
\t\t\t\t<ns3:metaDataName>status</ns3:metaDataName>
\t\t\t\t<ns3:metaDataValue>Tiffany Wood</ns3:metaDataValue>
\t\t\t</ns1:namedMetaData>
\t\t\t<ns1:locationAddress>
\t\t\t\t<ns4:street>None</ns4:street>
\t\t\t\t<ns4:houseNumber>.</ns4:houseNumber>
\t\t\t\t<ns4:town>None</ns4:town>
\t\t\t\t<ns4:swissZipCode>9999</ns4:swissZipCode>
\t\t\t\t<ns4:country>
\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t</ns4:country>
\t\t\t</ns1:locationAddress>
\t\t\t<ns1:realestateInformation>
\t\t\t\t<ns1:realestate>
\t\t\t\t\t<ns3:realestateIdentification>
\t\t\t\t\t\t<ns3:number>0</ns3:number>
\t\t\t\t\t</ns3:realestateIdentification>
\t\t\t\t\t<ns3:realestateType>8</ns3:realestateType>
\t\t\t\t</ns1:realestate>
\t\t\t\t<ns1:municipality>
\t\t\t\t\t<ns5:municipalityName>Elizabethburgh</ns5:municipalityName>
\t\t\t\t\t<ns5:cantonAbbreviation>SZ</ns5:cantonAbbreviation>
\t\t\t\t</ns1:municipality>
\t\t\t\t<ns1:owner>
\t\t\t\t\t<ns1:ownerAdress>
\t\t\t\t\t\t<ns4:person>
\t\t\t\t\t\t\t<ns4:firstName>unknown</ns4:firstName>
\t\t\t\t\t\t\t<ns4:lastName>unknown</ns4:lastName>
\t\t\t\t\t\t</ns4:person>
\t\t\t\t\t\t<ns4:addressInformation>
\t\t\t\t\t\t\t<ns4:street>unknown</ns4:street>
\t\t\t\t\t\t\t<ns4:houseNumber>0</ns4:houseNumber>
\t\t\t\t\t\t\t<ns4:town>unknown</ns4:town>
\t\t\t\t\t\t\t<ns4:swissZipCode>9999</ns4:swissZipCode>
\t\t\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t\t\t</ns4:country>
\t\t\t\t\t\t</ns4:addressInformation>
\t\t\t\t\t</ns1:ownerAdress>
\t\t\t\t</ns1:owner>
\t\t\t</ns1:realestateInformation>
\t\t\t<ns1:document>
\t\t\t\t<ns6:uuid>7c429fde-d404-4ddd-95cb-4f71a2fc0c39</ns6:uuid>
\t\t\t\t<ns6:titles>
\t\t\t\t\t<ns7:title>field</ns7:title>
\t\t\t\t</ns6:titles>
\t\t\t\t<ns6:status>signed</ns6:status>
\t\t\t\t<ns6:files>
\t\t\t\t\t<ns6:file>
\t\t\t\t\t\t<ns6:pathFileName>http://ebau.local/api/v1/attachments/files/?attachments=<!-- ATTACHMENT_ID --></ns6:pathFileName>
\t\t\t\t\t\t<ns6:mimeType>message/imdn+xml</ns6:mimeType>
\t\t\t\t\t</ns6:file>
\t\t\t\t</ns6:files>
\t\t\t\t<ns6:documentKind/>
\t\t\t</ns1:document>
\t\t\t<ns1:referencedPlanningPermissionApplication>
\t\t\t\t<ns1:localID>
\t\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t\t<ns3:Id>TEST-90-22-001</ns3:Id>
\t\t\t\t</ns1:localID>
\t\t\t\t<ns1:otherID>
\t\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t\t<ns3:Id>TEST-90-22-001</ns3:Id>
\t\t\t\t</ns1:otherID>
\t\t\t\t<ns1:dossierIdentification><!-- INSTANCE_ID --></ns1:dossierIdentification>
\t\t\t</ns1:referencedPlanningPermissionApplication>
\t\t</ns1:planningPermissionApplication>
\t\t<ns1:relationshipToPerson>
\t\t\t<ns1:role>applicant</ns1:role>
\t\t\t<ns1:person>
\t\t\t\t<ns3:identification>
\t\t\t\t\t<ns3:organisationIdentification>
\t\t\t\t\t\t<ns8:uid>
\t\t\t\t\t\t\t<ns8:uidOrganisationIdCategorie>CHE</ns8:uidOrganisationIdCategorie>
\t\t\t\t\t\t\t<ns8:uidOrganisationId>123123123</ns8:uidOrganisationId>
\t\t\t\t\t\t</ns8:uid>
\t\t\t\t\t\t<ns8:localOrganisationId>
\t\t\t\t\t\t\t<ns8:organisationIdCategory>unknown</ns8:organisationIdCategory>
\t\t\t\t\t\t\t<ns8:organisationId><!-- ORGANISATION_ID --></ns8:organisationId>
\t\t\t\t\t\t</ns8:localOrganisationId>
\t\t\t\t\t\t<ns8:organisationName>White Group</ns8:organisationName>
\t\t\t\t\t\t<ns8:organisationAdditionalName>Heather Marsh</ns8:organisationAdditionalName>
\t\t\t\t\t\t<ns8:legalForm>0223</ns8:legalForm>
\t\t\t\t\t</ns3:organisationIdentification>
\t\t\t\t</ns3:identification>
\t\t\t\t<ns3:address>
\t\t\t\t\t<ns4:street>Miller Centers</ns4:street>
\t\t\t\t\t<ns4:houseNumber>.</ns4:houseNumber>
\t\t\t\t\t<ns4:town>Thomasville</ns4:town>
\t\t\t\t\t<ns4:swissZipCode>1816</ns4:swissZipCode>
\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t</ns4:country>
\t\t\t\t</ns3:address>
\t\t\t</ns1:person>
\t\t</ns1:relationshipToPerson>
\t\t<ns1:relationshipToPerson>
\t\t\t<ns1:role>contact</ns1:role>
\t\t\t<ns1:person>
\t\t\t\t<ns3:identification>
\t\t\t\t\t<ns3:personIdentification>
\t\t\t\t\t\t<ns9:officialName>Liu</ns9:officialName>
\t\t\t\t\t\t<ns9:firstName>Jessica</ns9:firstName>
\t\t\t\t\t</ns3:personIdentification>
\t\t\t\t</ns3:identification>
\t\t\t\t<ns3:address>
\t\t\t\t\t<ns4:street>Scott Ridge</ns4:street>
\t\t\t\t\t<ns4:houseNumber>.</ns4:houseNumber>
\t\t\t\t\t<ns4:town>Lake Williamchester</ns4:town>
\t\t\t\t\t<ns4:swissZipCode>5731</ns4:swissZipCode>
\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t</ns4:country>
\t\t\t\t</ns3:address>
\t\t\t</ns1:person>
\t\t</ns1:relationshipToPerson>
\t\t<ns1:relationshipToPerson>
\t\t\t<ns1:role>project author</ns1:role>
\t\t\t<ns1:person>
\t\t\t\t<ns3:identification>
\t\t\t\t\t<ns3:personIdentification>
\t\t\t\t\t\t<ns9:officialName>Gilbert</ns9:officialName>
\t\t\t\t\t\t<ns9:firstName>Crystal</ns9:firstName>
\t\t\t\t\t</ns3:personIdentification>
\t\t\t\t</ns3:identification>
\t\t\t\t<ns3:address>
\t\t\t\t\t<ns4:street>Carl Port</ns4:street>
\t\t\t\t\t<ns4:houseNumber>.</ns4:houseNumber>
\t\t\t\t\t<ns4:town>Brownstad</ns4:town>
\t\t\t\t\t<ns4:swissZipCode>9394</ns4:swissZipCode>
\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t</ns4:country>
\t\t\t\t</ns3:address>
\t\t\t</ns1:person>
\t\t</ns1:relationshipToPerson>
\t\t<ns1:relationshipToPerson>
\t\t\t<ns1:role>landowner</ns1:role>
\t\t\t<ns1:person>
\t\t\t\t<ns3:identification>
\t\t\t\t\t<ns3:personIdentification>
\t\t\t\t\t\t<ns9:officialName>Lloyd</ns9:officialName>
\t\t\t\t\t\t<ns9:firstName>Ian</ns9:firstName>
\t\t\t\t\t</ns3:personIdentification>
\t\t\t\t</ns3:identification>
\t\t\t\t<ns3:address>
\t\t\t\t\t<ns4:street>Ryan Burgs</ns4:street>
\t\t\t\t\t<ns4:houseNumber>.</ns4:houseNumber>
\t\t\t\t\t<ns4:town>East Charlesburgh</ns4:town>
\t\t\t\t\t<ns4:swissZipCode>5416</ns4:swissZipCode>
\t\t\t\t\t<ns4:country>
\t\t\t\t\t\t<ns4:countryNameShort>CH</ns4:countryNameShort>
\t\t\t\t\t</ns4:country>
\t\t\t\t</ns3:address>
\t\t\t</ns1:person>
\t\t</ns1:relationshipToPerson>
\t</ns1:eventSubmitPlanningPermissionApplication>
</ns1:delivery>
'''

snapshots['test_task_event_handler_SBs[conclusion] 1'] = '''<?xml version="1.0" ?>
<ns1:delivery xmlns:ns1="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0129/5" xmlns:ns4="http://www.ech.ch/xmlns/eCH-0039/2" xmlns:ns5="http://www.ech.ch/xmlns/eCH-0147/T0/1">
\t<ns1:deliveryHeader>
\t\t<ns2:senderId>https://ebau.apps.be.ch/</ns2:senderId>
\t\t<ns2:messageId><!-- MESSAGE_ID --></ns2:messageId>
\t\t<ns2:messageType>5200009</ns2:messageType>
\t\t<ns2:sendingApplication>
\t\t\t<ns2:manufacturer>Adfinis AG</ns2:manufacturer>
\t\t\t<ns2:product>camac</ns2:product>
\t\t\t<ns2:productVersion><!-- VERSION --></ns2:productVersion>
\t\t</ns2:sendingApplication>
\t\t<ns2:subject>task</ns2:subject>
\t\t<ns2:messageDate>2022-06-03T00:00:00Z</ns2:messageDate>
\t\t<ns2:action>1</ns2:action>
\t\t<ns2:testDeliveryFlag>true</ns2:testDeliveryFlag>
\t</ns1:deliveryHeader>
\t<ns1:eventRequest>
\t\t<ns1:eventType>task</ns1:eventType>
\t\t<ns1:planningPermissionApplicationIdentification>
\t\t\t<ns1:localID>
\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t<ns3:Id>2020-1</ns3:Id>
\t\t\t</ns1:localID>
\t\t\t<ns1:otherID>
\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t<ns3:Id>2020-1</ns3:Id>
\t\t\t</ns1:otherID>
\t\t\t<ns1:dossierIdentification><!-- INSTANCE_ID --></ns1:dossierIdentification>
\t\t</ns1:planningPermissionApplicationIdentification>
\t\t<ns1:directive>
\t\t\t<uuid>00000000-0000-0000-0000-000000000000</uuid>
\t\t\t<instruction>process</instruction>
\t\t\t<priority>undefined</priority>
\t\t\t<comments>
\t\t\t\t<ns4:comment>SB2 eingereicht</ns4:comment>
\t\t\t</comments>
\t\t</ns1:directive>
\t\t<ns1:document>
\t\t\t<ns5:uuid>e8786da8-4cac-4b4c-aac3-cf7c66ac7eac</ns5:uuid>
\t\t\t<ns5:titles>
\t\t\t\t<ns4:title>against</ns4:title>
\t\t\t</ns5:titles>
\t\t\t<ns5:status>signed</ns5:status>
\t\t\t<ns5:files>
\t\t\t\t<ns5:file>
\t\t\t\t\t<ns5:pathFileName>http://ebau.local/api/v1/attachments/files/?attachments=<!-- ATTACHMENT_ID --></ns5:pathFileName>
\t\t\t\t\t<ns5:mimeType>audio/basic</ns5:mimeType>
\t\t\t\t</ns5:file>
\t\t\t</ns5:files>
\t\t\t<ns5:documentKind>David Gomez</ns5:documentKind>
\t\t</ns1:document>
\t</ns1:eventRequest>
</ns1:delivery>
'''

snapshots['test_task_event_handler_SBs[sb2] 1'] = '''<?xml version="1.0" ?>
<ns1:delivery xmlns:ns1="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0129/5" xmlns:ns4="http://www.ech.ch/xmlns/eCH-0039/2" xmlns:ns5="http://www.ech.ch/xmlns/eCH-0147/T0/1">
\t<ns1:deliveryHeader>
\t\t<ns2:senderId>https://ebau.apps.be.ch/</ns2:senderId>
\t\t<ns2:messageId><!-- MESSAGE_ID --></ns2:messageId>
\t\t<ns2:messageType>5200008</ns2:messageType>
\t\t<ns2:sendingApplication>
\t\t\t<ns2:manufacturer>Adfinis AG</ns2:manufacturer>
\t\t\t<ns2:product>camac</ns2:product>
\t\t\t<ns2:productVersion><!-- VERSION --></ns2:productVersion>
\t\t</ns2:sendingApplication>
\t\t<ns2:subject>task</ns2:subject>
\t\t<ns2:messageDate>2022-06-03T00:00:00Z</ns2:messageDate>
\t\t<ns2:action>1</ns2:action>
\t\t<ns2:testDeliveryFlag>true</ns2:testDeliveryFlag>
\t</ns1:deliveryHeader>
\t<ns1:eventRequest>
\t\t<ns1:eventType>task</ns1:eventType>
\t\t<ns1:planningPermissionApplicationIdentification>
\t\t\t<ns1:localID>
\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t<ns3:Id>2020-1</ns3:Id>
\t\t\t</ns1:localID>
\t\t\t<ns1:otherID>
\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t<ns3:Id>2020-1</ns3:Id>
\t\t\t</ns1:otherID>
\t\t\t<ns1:dossierIdentification><!-- INSTANCE_ID --></ns1:dossierIdentification>
\t\t</ns1:planningPermissionApplicationIdentification>
\t\t<ns1:directive>
\t\t\t<uuid>00000000-0000-0000-0000-000000000000</uuid>
\t\t\t<instruction>process</instruction>
\t\t\t<priority>undefined</priority>
\t\t\t<comments>
\t\t\t\t<ns4:comment>SB1 eingereicht</ns4:comment>
\t\t\t</comments>
\t\t</ns1:directive>
\t\t<ns1:document>
\t\t\t<ns5:uuid>8463f903-f637-4103-b8a9-39dece3eeffb</ns5:uuid>
\t\t\t<ns5:titles>
\t\t\t\t<ns4:title>country</ns4:title>
\t\t\t</ns5:titles>
\t\t\t<ns5:status>signed</ns5:status>
\t\t\t<ns5:files>
\t\t\t\t<ns5:file>
\t\t\t\t\t<ns5:pathFileName>http://ebau.local/api/v1/attachments/files/?attachments=<!-- ATTACHMENT_ID --></ns5:pathFileName>
\t\t\t\t\t<ns5:mimeType>image/png</ns5:mimeType>
\t\t\t\t</ns5:file>
\t\t\t</ns5:files>
\t\t\t<ns5:documentKind>Daniel Mann</ns5:documentKind>
\t\t</ns1:document>
\t</ns1:eventRequest>
</ns1:delivery>
'''

snapshots['test_task_event_handler_stellungnahme 1'] = '''<?xml version="1.0" ?>
<ns1:delivery xmlns:ns1="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0129/5" xmlns:ns4="http://www.ech.ch/xmlns/eCH-0039/2" xmlns:ns5="http://www.ech.ch/xmlns/eCH-0147/T0/1">
\t<ns1:deliveryHeader>
\t\t<ns2:senderId>https://ebau.apps.be.ch/</ns2:senderId>
\t\t<ns2:messageId><!-- MESSAGE_ID --></ns2:messageId>
\t\t<ns2:messageType>5200007</ns2:messageType>
\t\t<ns2:sendingApplication>
\t\t\t<ns2:manufacturer>Adfinis AG</ns2:manufacturer>
\t\t\t<ns2:product>camac</ns2:product>
\t\t\t<ns2:productVersion><!-- VERSION --></ns2:productVersion>
\t\t</ns2:sendingApplication>
\t\t<ns2:subject>task</ns2:subject>
\t\t<ns2:messageDate>2022-06-03T00:00:00Z</ns2:messageDate>
\t\t<ns2:action>1</ns2:action>
\t\t<ns2:testDeliveryFlag>true</ns2:testDeliveryFlag>
\t</ns1:deliveryHeader>
\t<ns1:eventRequest>
\t\t<ns1:eventType>task</ns1:eventType>
\t\t<ns1:planningPermissionApplicationIdentification>
\t\t\t<ns1:localID>
\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t<ns3:Id>2020-1</ns3:Id>
\t\t\t</ns1:localID>
\t\t\t<ns1:otherID>
\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t<ns3:Id>2020-1</ns3:Id>
\t\t\t</ns1:otherID>
\t\t\t<ns1:dossierIdentification><!-- INSTANCE_ID --></ns1:dossierIdentification>
\t\t</ns1:planningPermissionApplicationIdentification>
\t\t<ns1:directive>
\t\t\t<uuid>00000000-0000-0000-0000-000000000000</uuid>
\t\t\t<instruction>process</instruction>
\t\t\t<priority>undefined</priority>
\t\t\t<deadline>1985-06-26</deadline>
\t\t\t<comments>
\t\t\t\t<ns4:comment>Anforderung einer Stellungnahme</ns4:comment>
\t\t\t</comments>
\t\t</ns1:directive>
\t\t<ns1:document>
\t\t\t<ns5:uuid>50e761c4-c03e-4757-aa06-9a30e9c269ca</ns5:uuid>
\t\t\t<ns5:titles>
\t\t\t\t<ns4:title>buy</ns4:title>
\t\t\t</ns5:titles>
\t\t\t<ns5:status>signed</ns5:status>
\t\t\t<ns5:files>
\t\t\t\t<ns5:file>
\t\t\t\t\t<ns5:pathFileName>http://ebau.local/api/v1/attachments/files/?attachments=<!-- ATTACHMENT_ID --></ns5:pathFileName>
\t\t\t\t\t<ns5:mimeType>message/rfc822</ns5:mimeType>
\t\t\t\t</ns5:file>
\t\t\t</ns5:files>
\t\t\t<ns5:documentKind>Rebecca Gonzalez</ns5:documentKind>
\t\t</ns1:document>
\t</ns1:eventRequest>
</ns1:delivery>
'''
