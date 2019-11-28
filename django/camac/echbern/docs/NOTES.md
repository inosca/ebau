# Gemeindeschnittstelle eBau

## Authentifizierung

Zur Authentifizierung wird der Standard [OpenID Connect](https://openid.net/connect/) genutzt. Pro Gemeindesoftware wird eine `client-id` und ein `client-secret` vergeben, mit welchen Tokens bezogen werden können:

```bash
curl --request POST \
--url 'https://ebau-test.sycloud.ch/auth/realms/camac/protocol/openid-connect/token' \
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

## Abweichungen udn Besonderheiten

- Der Typ `planningPermissionAplicationIdentifier` enthält unter `localId` unsere Dossiernummer ("Instance id")

- Der Type `localOrganisationId` enthält unter `organisationId` unsere Service id. Service ids können über den `/ech/v1/public-services/` endpoint abgefragt werden.

- Der von uns empfangene Typ `task`, um Stellungnahmen anzufordern (Spezifikation 3.2) muss zwingend die Service id der einzuladenden Stelle im `extension` Typ enthalten:

    ```xml
    <ns2:extension>
      <serviceId>23</serviceId>
    </ns2:extension>
    ```

- Der eCH-Standard forciert, dass bei den meisten Meldungen ein `document` mitgeschickt wird. Dieses `document` wird (mit Ausnahme von `accompanyingReport`) von eBau ignoriert.

- In einer `application` wird immer der Status `6701` gesetzt. Der korrekte Status aus dem eBau findet sich unter `namedMetaData.status`. Bei einer `statusNotification` wird immer der Status `in progress` gesetzt. Der korrekte Status findet sich im `remark`.

- `messageType` beinhaltet bei den von uns generierten Meldungen immer den Meldungstyp (`changeResponsibility`, `statusNotification`, etc). Bei empfangenen Meldungen wird das property ignoriert.


## Messages

### GET

{get_messages}

### POST

{post_messages}
