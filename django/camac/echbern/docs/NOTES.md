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

## Group Parameter

Bei den meisten Endpunkten, lässt sich über den `group` Parameter angeben, im Namen welcher Gruppe ein Request gemacht werden soll.

Dies ist notwendig, um die verschiedenen Stellen innerhalb einer Gemeinde zu unterscheiden. Alle Meldungen nach Erteilung eines positiven Bauentscheids werden an die Baukontrolle adressiert.

### Beispiel

 - Gemeinde client `A` hat als Standardgruppe `Leitung Leitbehörde Gemeinde A`
 - Zusätzlich besteht noch eine Mitgliedschaft in der Gruppe `Leitung Baukontrolle Gemeinde A`
 - Requests mit dem client dieser Gemeinde werden standardmässig im Namen der Gruppe `Leitung Leitbehörde Gemeinde A` gemacht
 - Sollen nun beispielsweise Meldungen für die Gruppe `Leitung Baukontrolle Gemeinde A` abgeholt werden, muss der `group` Parameter entsprechend gesetzt werden

### Abfragen von Gruppen IDs

Unter dem Tag [User](#/User) sind die Endpunkte zusammengefasst, die eine Abfrage von Gruppenmitgliedschaften und -IDs ermöglichen:

 - [/me](#/User/api_v1_me_read) zeigt Informationen zum aktuellen User, inklusive Gruppenmitgliedschaften, an
 - [/groups](#/User/api_v1_groups_list) zeigt alle Gruppen an, für welche eine Mitgliedschaft besteht
 - [/groups/{group_id}](#/User/api_v1_groups_read) zeigt Informationen zu einer spezifischen Gruppe an

### Direktlinks in eBau

Verschiedene Aufgaben werden gemäss Spezifikation direkt in eBau erledigt. Unterstützt werden folgende Links:

- `/ech/v1/instance/<instance_id>/`: Allgemeiner Link auf ein Dossier, Einstieg für Dossierkorrektur (Kap. 3.1)
- `/ech/v1/ebau-number/<instance_id>/`: eBau-Nummer vergeben (Kap. 3.1)
- `/ech/v1/claim/<instance_id>/`: Nachforderungsseite (Kap. 3.1, 3.3.2)
- `/ech/v1/dossier-check/<instance_id>/`: Dossierprüfung (formelle und materielle Prüfung, Kap. 3.1)
- `/ech/v1/revision-history/<instance_id>/`: Änderungsverlauf von Dossier

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

- `buildingCategory` wird immer auf `1040` gesetzt.

- `documentStatusType` wird immer auf `signed` gesetzt.

- `realestateType` wird immer auf `8` gesetzt.

- Properties, die in eCH zwingend sind, in eBau jedoch nicht, werden bei nichtvorhandensein mit `unknown` befüllt.

- In eBau ist es möglich, auch ausländische Adressen zu erfassen. Bei solchen wird die Postleitzahl auf `9999` gesetzt, falls sie nicht vierstellig sein sollte.

- In eCH ist es nicht möglich, Kosten von unter 1000.- zu erfassen. Sollten die in eBau erfassten Kosten tiefer als 1000.- sein, wird `1000` eingetragen.

- Relevante URLs finden sich in den Meldungen im `HeaderType` unter `extension`.

- 4.2 Bauverfahren abschliessen: Bei Voranfragen wird der Prozess mit einem Entscheid (bzw. fachlich einer Beurteilung) abgeschlossen. "close dossier" hat entgegen der Spezifikation für Voranfragen also keine Bedeutung. Stattdessen wird der Prozess mit "notice ruling" abgeschlossen (siehe Kap. 3.2).

- 5.3.5 Rückzug des Baugesuchs: Diese Funktion ist nicht in eBau implementiert, darum kann diese Message nicht ausgeliefert werden.

- Judgements in `NoticeRuling` werden in eBau wie folgt gemappt:

    | Judgement | Descision               | Besonderheiten                     |
    |-----------|-------------------------|------------------------------------|
    | 1         | Bewilligt               |                                    |
    | 2         | Bewilligt mit Vorbehalt | Nicht verfügbar für Baugesuche     |
    | 3         | Abgeschrieben           | Nicht verfügbar für Vorabklärungen |
    | 4         | Abgelehnt               |                                    |

 - `relationshipToPerson`: Hier füllen wir folgende Personalien ab:

    | eBau form              | ech role       |
    |------------------------|----------------|
    | Gesuchsteller          | applicant      |
    | Vertreter mit Vollmacht| contact        |
    | Projektverfasser       | project author |
    | Grundeigentümer        | landowner      |

    Sollte es sich bei einem Eintrag um eine juristische Person handeln, sieht eCH keine
    Felder vor für Vor- und Nachname der Kontaktperson. Wir füllen diese Namen daher in das Feld
    `organisationAdditionalName` im Format: "Vorname Name".


## Message Typen

### GET

{get_messages}

### POST

Der Parameter `messageType` wird bei der Auswertung ignoriert - entscheidend ist der `event type` sowie, falls nötig, zusätzliche Parameter (z.B. `judgement` bei `NoticeRuling`).

{post_messages}
