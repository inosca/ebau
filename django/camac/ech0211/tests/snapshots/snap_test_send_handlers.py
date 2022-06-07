# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_accompanying_report_send_handler[True-True] 1'] = '''<?xml version="1.0" ?>
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
\t\t\t\t<ns3:Id>unknown</ns3:Id>
\t\t\t</ns1:localID>
\t\t\t<ns1:otherID>
\t\t\t\t<ns3:IdCategory>eBauNr</ns3:IdCategory>
\t\t\t\t<ns3:Id>unknown</ns3:Id>
\t\t\t</ns1:otherID>
\t\t\t<ns1:dossierIdentification><!-- INSTANCE_ID --></ns1:dossierIdentification>
\t\t</ns1:planningPermissionApplicationIdentification>
\t\t<ns1:document>
\t\t\t<ns4:uuid>00000000-0000-0000-0000-000000000000</ns4:uuid>
\t\t\t<ns4:titles>
\t\t\t\t<ns5:title>MyFile</ns5:title>
\t\t\t</ns4:titles>
\t\t\t<ns4:status>signed</ns4:status>
\t\t\t<ns4:files>
\t\t\t\t<ns4:file>
\t\t\t\t\t<ns4:pathFileName>http://ebau.local/api/v1/attachments/files/?attachments=<!-- ATTACHMENT_ID --></ns4:pathFileName>
\t\t\t\t\t<ns4:mimeType>model/x3d+vrml</ns4:mimeType>
\t\t\t\t</ns4:file>
\t\t\t</ns4:files>
\t\t\t<ns4:documentKind>Ashley Stewart</ns4:documentKind>
\t\t</ns1:document>
\t\t<ns1:remark>Wird in das Feld &quot;Stellungnahme&quot; übernommen.</ns1:remark>
\t\t<ns1:ancillaryClauses>Wird in das Feld &quot;Nebenbestimmungen&quot; übernommen.; Wird in das Feld &quot;Nebenbestimmungen&quot; übernommen.</ns1:ancillaryClauses>
\t</ns1:eventAccompanyingReport>
</ns1:delivery>
'''

snapshots['test_change_responsibility_send_handler[True-circulation_init-True-True] 1'] = '''<?xml version="1.0" ?>
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
\t\t\t\t\t<ns4:organisationName>Peter Alvarez</ns4:organisationName>
\t\t\t\t\t<ns4:legalForm>0223</ns4:legalForm>
\t\t\t\t</ns3:buildingAuthorityIdentificationType>
\t\t\t\t<ns3:address>
\t\t\t\t\t<ns6:street>None</ns6:street>
\t\t\t\t\t<ns6:town>Estradaport</ns6:town>
\t\t\t\t\t<ns6:country>
\t\t\t\t\t\t<ns6:countryNameShort>CH</ns6:countryNameShort>
\t\t\t\t\t</ns6:country>
\t\t\t\t</ns3:address>
\t\t\t</ns1:decisionAuthority>
\t\t</ns1:responsibleDecisionAuthority>
\t</ns1:eventChangeResponsibility>
</ns1:delivery>
'''

snapshots['test_close_dossier_send_handler[baukontrolle-conclusion-True] 1'] = '''<?xml version="1.0" ?>
<ns1:delivery xmlns:ns1="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0129/5">
\t<ns1:deliveryHeader>
\t\t<ns2:senderId>https://ebau.apps.be.ch/</ns2:senderId>
\t\t<ns2:messageId><!-- MESSAGE_ID --></ns2:messageId>
\t\t<ns2:messageType>5200036</ns2:messageType>
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
\t\t<ns1:remark>finished</ns1:remark>
\t</ns1:eventStatusNotification>
</ns1:delivery>
'''

snapshots['test_close_dossier_send_handler[leitbehoerde-sb1-True] 1'] = '''<?xml version="1.0" ?>
<ns1:delivery xmlns:ns1="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0129/5">
\t<ns1:deliveryHeader>
\t\t<ns2:senderId>https://ebau.apps.be.ch/</ns2:senderId>
\t\t<ns2:messageId><!-- MESSAGE_ID --></ns2:messageId>
\t\t<ns2:messageType>5200036</ns2:messageType>
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
\t\t<ns1:remark>finished</ns1:remark>
\t</ns1:eventStatusNotification>
</ns1:delivery>
'''

snapshots['test_kind_of_proceedings_send_handler[True] 1'] = '''<?xml version="1.0" ?>
<ns1:delivery xmlns:ns1="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0129/5">
\t<ns1:deliveryHeader>
\t\t<ns2:senderId>https://ebau.apps.be.ch/</ns2:senderId>
\t\t<ns2:messageId><!-- MESSAGE_ID --></ns2:messageId>
\t\t<ns2:messageType>5200032</ns2:messageType>
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
\t\t<ns1:remark>circulation</ns1:remark>
\t</ns1:eventStatusNotification>
</ns1:delivery>
'''

snapshots['test_notice_ruling_send_handler[1-circulation-True-False-leitbehoerde-sb1-municipality] 1'] = '''<?xml version="1.0" ?>
<ns1:delivery xmlns:ns1="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0129/5">
\t<ns1:deliveryHeader>
\t\t<ns2:senderId>https://ebau.apps.be.ch/</ns2:senderId>
\t\t<ns2:messageId><!-- MESSAGE_ID --></ns2:messageId>
\t\t<ns2:messageType>5200033</ns2:messageType>
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
\t\t<ns1:remark>sb1</ns1:remark>
\t</ns1:eventStatusNotification>
</ns1:delivery>
'''

snapshots['test_notice_ruling_send_handler[1-circulation-True-False-rsta-sb1-municipality] 1'] = '''<?xml version="1.0" ?>
<ns1:delivery xmlns:ns1="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0129/5">
\t<ns1:deliveryHeader>
\t\t<ns2:senderId>https://ebau.apps.be.ch/</ns2:senderId>
\t\t<ns2:messageId><!-- MESSAGE_ID --></ns2:messageId>
\t\t<ns2:messageType>5200033</ns2:messageType>
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
\t\t<ns1:remark>sb1</ns1:remark>
\t</ns1:eventStatusNotification>
</ns1:delivery>
'''

snapshots['test_notice_ruling_send_handler[1-circulation-True-True-leitbehoerde-evaluated-municipality] 1'] = '''<?xml version="1.0" ?>
<ns1:delivery xmlns:ns1="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0129/5">
\t<ns1:deliveryHeader>
\t\t<ns2:senderId>https://ebau.apps.be.ch/</ns2:senderId>
\t\t<ns2:messageId><!-- MESSAGE_ID --></ns2:messageId>
\t\t<ns2:messageType>5200036</ns2:messageType>
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
\t\t<ns1:remark>evaluated</ns1:remark>
\t</ns1:eventStatusNotification>
</ns1:delivery>
'''

snapshots['test_notice_ruling_send_handler[1-coordination-True-False-leitbehoerde-sb1-municipality] 1'] = '''<?xml version="1.0" ?>
<ns1:delivery xmlns:ns1="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0129/5">
\t<ns1:deliveryHeader>
\t\t<ns2:senderId>https://ebau.apps.be.ch/</ns2:senderId>
\t\t<ns2:messageId><!-- MESSAGE_ID --></ns2:messageId>
\t\t<ns2:messageType>5200033</ns2:messageType>
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
\t\t<ns1:remark>sb1</ns1:remark>
\t</ns1:eventStatusNotification>
</ns1:delivery>
'''

snapshots['test_notice_ruling_send_handler[4-circulation_init-True-False-leitbehoerde-rejected-municipality] 1'] = '''<?xml version="1.0" ?>
<ns1:delivery xmlns:ns1="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0129/5">
\t<ns1:deliveryHeader>
\t\t<ns2:senderId>https://ebau.apps.be.ch/</ns2:senderId>
\t\t<ns2:messageId><!-- MESSAGE_ID --></ns2:messageId>
\t\t<ns2:messageType>5200037</ns2:messageType>
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
\t\t<ns1:remark>rejected</ns1:remark>
\t</ns1:eventStatusNotification>
</ns1:delivery>
'''

snapshots['test_task_send_handler[latest_empty-True-True-True] 1'] = '''<?xml version="1.0" ?>
<ns1:delivery xmlns:ns1="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0129/5" xmlns:ns4="http://www.ech.ch/xmlns/eCH-0039/2">
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
\t\t<ns2:messageDate>2020-02-23T22:09:01.123456Z</ns2:messageDate>
\t\t<ns2:action>1</ns2:action>
\t\t<ns2:testDeliveryFlag>true</ns2:testDeliveryFlag>
\t</ns1:deliveryHeader>
\t<ns1:eventRequest>
\t\t<ns1:eventType>task</ns1:eventType>
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
\t\t<ns1:directive>
\t\t\t<uuid>00000000-0000-0000-0000-000000000000</uuid>
\t\t\t<instruction>process</instruction>
\t\t\t<priority>undefined</priority>
\t\t\t<deadline>2020-03-23</deadline>
\t\t\t<comments>
\t\t\t\t<ns4:comment>Anforderung einer Stellungnahme</ns4:comment>
\t\t\t</comments>
\t\t</ns1:directive>
\t</ns1:eventRequest>
</ns1:delivery>
'''

snapshots['test_task_send_handler[latest_not_running-True-True-True] 1'] = '''<?xml version="1.0" ?>
<ns1:delivery xmlns:ns1="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0129/5" xmlns:ns4="http://www.ech.ch/xmlns/eCH-0039/2">
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
\t\t<ns2:messageDate>2020-02-23T22:09:01.123456Z</ns2:messageDate>
\t\t<ns2:action>1</ns2:action>
\t\t<ns2:testDeliveryFlag>true</ns2:testDeliveryFlag>
\t</ns1:deliveryHeader>
\t<ns1:eventRequest>
\t\t<ns1:eventType>task</ns1:eventType>
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
\t\t<ns1:directive>
\t\t\t<uuid>00000000-0000-0000-0000-000000000000</uuid>
\t\t\t<instruction>process</instruction>
\t\t\t<priority>undefined</priority>
\t\t\t<deadline>2020-03-23</deadline>
\t\t\t<comments>
\t\t\t\t<ns4:comment>Anforderung einer Stellungnahme</ns4:comment>
\t\t\t</comments>
\t\t</ns1:directive>
\t</ns1:eventRequest>
</ns1:delivery>
'''

snapshots['test_task_send_handler[latest_running-True-True-True] 1'] = '''<?xml version="1.0" ?>
<ns1:delivery xmlns:ns1="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0129/5" xmlns:ns4="http://www.ech.ch/xmlns/eCH-0039/2">
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
\t\t<ns2:messageDate>2020-02-23T22:09:01.123456Z</ns2:messageDate>
\t\t<ns2:action>1</ns2:action>
\t\t<ns2:testDeliveryFlag>true</ns2:testDeliveryFlag>
\t</ns1:deliveryHeader>
\t<ns1:eventRequest>
\t\t<ns1:eventType>task</ns1:eventType>
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
\t\t<ns1:directive>
\t\t\t<uuid>00000000-0000-0000-0000-000000000000</uuid>
\t\t\t<instruction>process</instruction>
\t\t\t<priority>undefined</priority>
\t\t\t<deadline>2020-03-23</deadline>
\t\t\t<comments>
\t\t\t\t<ns4:comment>Anforderung einer Stellungnahme</ns4:comment>
\t\t\t</comments>
\t\t</ns1:directive>
\t</ns1:eventRequest>
</ns1:delivery>
'''

snapshots['test_task_send_handler[no_existing-True-True-True] 1'] = '''<?xml version="1.0" ?>
<ns1:delivery xmlns:ns1="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0129/5" xmlns:ns4="http://www.ech.ch/xmlns/eCH-0039/2">
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
\t\t<ns2:messageDate>2020-02-23T22:09:01.123456Z</ns2:messageDate>
\t\t<ns2:action>1</ns2:action>
\t\t<ns2:testDeliveryFlag>true</ns2:testDeliveryFlag>
\t</ns1:deliveryHeader>
\t<ns1:eventRequest>
\t\t<ns1:eventType>task</ns1:eventType>
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
\t\t<ns1:directive>
\t\t\t<uuid>00000000-0000-0000-0000-000000000000</uuid>
\t\t\t<instruction>process</instruction>
\t\t\t<priority>undefined</priority>
\t\t\t<deadline>2020-03-23</deadline>
\t\t\t<comments>
\t\t\t\t<ns4:comment>Anforderung einer Stellungnahme</ns4:comment>
\t\t\t</comments>
\t\t</ns1:directive>
\t</ns1:eventRequest>
</ns1:delivery>
'''

snapshots['test_task_send_handler[none_running-True-True-True] 1'] = '''<?xml version="1.0" ?>
<ns1:delivery xmlns:ns1="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0129/5" xmlns:ns4="http://www.ech.ch/xmlns/eCH-0039/2">
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
\t\t<ns2:messageDate>2020-02-23T22:09:01.123456Z</ns2:messageDate>
\t\t<ns2:action>1</ns2:action>
\t\t<ns2:testDeliveryFlag>true</ns2:testDeliveryFlag>
\t</ns1:deliveryHeader>
\t<ns1:eventRequest>
\t\t<ns1:eventType>task</ns1:eventType>
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
\t\t<ns1:directive>
\t\t\t<uuid>00000000-0000-0000-0000-000000000000</uuid>
\t\t\t<instruction>process</instruction>
\t\t\t<priority>undefined</priority>
\t\t\t<deadline>2020-03-23</deadline>
\t\t\t<comments>
\t\t\t\t<ns4:comment>Anforderung einer Stellungnahme</ns4:comment>
\t\t\t</comments>
\t\t</ns1:directive>
\t</ns1:eventRequest>
</ns1:delivery>
'''
