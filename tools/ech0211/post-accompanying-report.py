#!/usr/bin/env python3

from utils import each_client, endpoint, print_response, print_title

instance_id = 12
special_id = "2026-1"
document_uuid = "c11b2559-aeb8-43f6-a73f-37cca84f9e9e"

xml_payload = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
  <ns2:delivery xmlns:ns2="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns4="http://www.ech.ch/xmlns/eCH-0010/6" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0129/5" xmlns:ns6="http://www.ech.ch/xmlns/eCH-0044/4" xmlns:ns5="http://www.ech.ch/xmlns/eCH-0007/6" xmlns:ns8="http://www.ech.ch/xmlns/eCH-0008/3" xmlns:ns7="http://www.ech.ch/xmlns/eCH-0097/2" xmlns:ns13="http://www.ech.ch/xmlns/eCH-0046/1" xmlns:ns9="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:ns12="http://www.ech.ch/xmlns/eCH-0044/1" xmlns:ns11="http://www.ech.ch/xmlns/eCH-0147/T0/1" xmlns:ns10="http://www.ech.ch/xmlns/eCH-0039/2" xmlns:ns15="http://www.ech.ch/xmlns/eCH-0058/3" xmlns:ns14="http://www.ech.ch/xmlns/eCH-0010/3">
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
      <ns9:messageDate>2019-11-13T00:00:00.000Z</ns9:messageDate>
      <ns9:action>1</ns9:action>
      <ns9:testDeliveryFlag>true</ns9:testDeliveryFlag>
    </ns2:deliveryHeader>
    <ns2:eventAccompanyingReport>
      <ns2:eventType>accompanying report</ns2:eventType><!-- wird ignoriert -->
      <ns2:planningPermissionApplicationIdentification>
        <ns2:localID>
          <ns3:IdCategory>Category</ns3:IdCategory>
          <ns3:Id>{special_id}</ns3:Id>
        </ns2:localID>
        <ns2:otherID>
          <ns3:IdCategory>Category</ns3:IdCategory>
          <ns3:Id>{special_id}</ns3:Id>
        </ns2:otherID>
        <ns2:dossierIdentification>{instance_id}</ns2:dossierIdentification>
      </ns2:planningPermissionApplicationIdentification>
      <ns2:document>
        <!-- muss auf dem Dossier existieren -->
        <ns11:uuid>{document_uuid}</ns11:uuid>
        <ns11:titles>
          <ns10:title ns10:lang="de">Example.pdf</ns10:title>
        </ns11:titles>
        <ns11:status>created</ns11:status>
        <ns11:files>
          <ns11:file>
            <ns11:pathFileName>https://www.ech.ch/sites/default/files/imce/eCH-Dossier/eCH-Dossier_PDF_Publikationen/Hauptdokument/STAN_d_REP_2022-06-02_eCH-0211_V3.0.0_Baugesuch_0.pdf</ns11:pathFileName>
            <ns11:mimeType>application/pdf</ns11:mimeType>
            <ns11:version>1.0.0</ns11:version>
          </ns11:file>
        </ns11:files>
        <ns11:comments>
          <ns10:comment ns10:lang="DE">Dokumentkommentar</ns10:comment>
        </ns11:comments>
        <ns11:keywords>
          <ns10:keyword ns10:lang="DE">Gesuchsunterlagen vom: dd.mm.yyyy</ns10:keyword>
        </ns11:keywords>
        <ns11:documentKind>Weitere Dokumente</ns11:documentKind>
      </ns2:document>
      <ns2:remark>Wird in das Feld "Stellungnahme" übernommen.</ns2:remark>
      <ns2:ancillaryClauses>Wird in das Feld "Nebenbestimmungen" übernommen.</ns2:ancillaryClauses>
      <ns2:ancillaryClauses>Wird in das Feld "Nebenbestimmungen" übernommen.</ns2:ancillaryClauses>
      <ns2:extension>
        <situation>Wird aus dem Feld "Sachverhalt" abgefüllt.</situation>
        <considerations>Wird aus dem Feld "Erwägungen" abgefüllt.</considerations>
        <comments>Wird aus dem Feld "Bemerkungen" abgefüllt.</comments>
        <documentsAvailable>true</documentsAvailable>
      </ns2:extension>
    </ns2:eventAccompanyingReport>
  </ns2:delivery>
"""

print_title("eCH0211 - POST accompanying report")

for session, client_id in each_client():
    print(f" > perform request[accompanying report] for client_id: {client_id}")

    response = session.post(
        f"{endpoint}/ech/v1/send/",
        data=xml_payload.encode("utf-8"),
        headers={
            "accept": "application/xml",
            "content-type": "application/xml",
        },
    )

    print_response(response)
