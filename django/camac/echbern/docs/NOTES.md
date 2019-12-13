# Gemeindeschnittstelle eBau

## Authentifizierung

Zur Authentifizierung wird der Standard [OpenID Connect](https://openid.net/connect/) genutzt. Pro Gemeinde wird eine `client-id` und ein `client-secret` vergeben, mit welchen Tokens bezogen werden können:

```bash
curl --request POST \
--url 'https://portal.ebau-test.sycloud.ch/auth/realms/camac/protocol/openid-connect/token' \
--header 'content-type: application/x-www-form-urlencoded' \
--data grant_type=client_credentials \
--data client_id='${client-id}' \
--data client_secret=${client-secret}
```

Mit einem gültigen Token können API-Abfragen gemacht werden. Nachfolgend ein paar Beispiele:

## Sichtbare Gesuche auflisten

```bash
curl -X GET "https://ebau-test.sycloud.ch/ech/v1/applications?group=123" -H "Authorization: Bearer ${TOKEN}"
```

## Gesuch-Details abfragen (BaseDelivery)

```bash
curl -X GET "https://ebau-test.sycloud.ch/ech/v1/application/XYZ?group=123" -H "Authorization: Bearer ${TOKEN}"
```

## Abweichungen und Besonderheiten

- Der Type `planningPermissionAplicationIdentifier` enthält unter `localId` die eBau-Nummer und unter `dossierIdentification` unsere Dossiernummer ("Instance id")

- Der Type `localOrganisationId` enthält unter `organisationId` unsere Service id. Service ids können über den `/ech/v1/public-services/` endpoint abgefragt werden.

- Der von uns empfangene Typ `task`, um Stellungnahmen anzufordern (Spezifikation 3.2) muss zwingend die Service id der einzuladenden Stelle im `extension` Typ enthalten:

    ```xml
    <ns2:extension>
      <serviceId>23</serviceId>
    </ns2:extension>
    ```

- Der eCH-Standard forciert, dass bei den meisten Meldungen ein `document` mitgeschickt wird. Dieses `document` wird (mit Ausnahme von `accompanyingReport`) von eBau ignoriert. Dokumente werden über unsere API hoch- und heruntergeladen. Beim Hochladen werden sie bereits einer `Instance`, sowie einer oder mehreren `AttachmentSection` zugewiesen. Somit sind Dokumente in eCH Meldungen, die von eBau erhalten werden, redundant und werden ignoriert.

  Bei ausgehenden Meldungen werden die Dokumente jedoch korrekt abgefüllt. Dabei gilt zu beachten:
   - `documentKind` enthält alle `AttachmentSections`, separiert durch `; `
   - `keywords` enthält alle Tags (zB: `vollmacht-dokument`)
   - `uuid` enthält eine mit dem `Attachment` assoziierte uuid, diese ist jedoch ansonstenn nicht über die API exposed. `Attachments` werden prinzipiell über ihren PK referenziert

- In einer `application` wird immer der Status `6701` gesetzt. Der korrekte Status aus dem eBau findet sich unter `namedMetaData.status`. Bei einer `statusNotification` wird immer der Status `in progress` gesetzt. Der korrekte Status findet sich im `remark`.

- `messageType` beinhaltet bei den von uns generierten Meldungen immer den Meldungstyp (`changeResponsibility`, `statusNotification`, etc). Bei empfangenen Meldungen wird das property ignoriert.

- `buildingCategory` wird immer auf `1040` gesetzt.

- `documentStatusType` wird immer auf `signed` gesetzt.

- `realestateType` wird immer auf `8` gesetzt.

- Properties, die in eCH zwingend sind, in eBau jedoch nicht, werden bei nichtvorhandensein mit `unknown` befüllt.

- In eBau ist es möglich, auch ausländische Adressen zu erfassen. Bei solchen wird die Postleitzahl auf `9999` gesetzt, falls sie nicht vierstellig sein sollte.

- In eCH ist es nicht möglich, Kosten von unter 1000.- zu erfassen. Sollten die in eBau erfassten Kosten tiefer als 1000.- sein, wird `1000` eingetragen.

- Relevante URLs finden sich in den Meldungen im `HeaderType` unter `extension`.

## Messages

### GET

{get_messages}

### POST

{post_messages}
