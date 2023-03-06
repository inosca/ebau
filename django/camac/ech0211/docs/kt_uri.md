# URec REST API

## Authentifizierung

Zur Authentifizierung wird der Standard [OpenID Connect](https://openid.net/connect/) genutzt. Für den Zugang wird eine `client-id` und ein `client-secret` vergeben, mit welchen Tokens bezogen werden können:

```bash
curl --request POST \
--url 'https://urec.ur.sycloud.ch/auth/realms/urec/protocol/openid-connect/token' \
--header 'content-type: application/x-www-form-urlencoded' \
--data grant_type=client_credentials \
--data scope=openid \
--data client_id='${client-id}' \
--data client_secret=${client-secret}
```

Mit einem gültigen Token können API-Abfragen gemacht werden. Z.B. kann wie folgt eine Liste von Dokumenten abgefragt werden:

```bash
curl -X GET "https://urec.ur.sycloud.ch/api/v1/attachments?group=123" -H "Authorization: Bearer ${TOKEN}"
```

## Group Parameter

Bei den meisten Endpunkten, lässt sich über den `group` Parameter angeben, im Namen welcher Gruppe ein Request gemacht werden soll.

Dies ist dann notwendig, wenn der client in mehreren Gruppen berechtigt ist und je nach Situation auf Informationen zugreifen muss, welche nur bestimmten Gruppen zugänglich sind.

### Abfragen von Gruppen IDs

Unter dem Tag [User](#/User) sind die Endpunkte zusammengefasst, die eine Abfrage von Gruppenmitgliedschaften und -IDs ermöglichen:

- [/me](#/User/api_v1_me_read) zeigt Informationen zum aktuellen User, inklusive Gruppenmitgliedschaften, an
- [/groups](#/User/api_v1_groups_list) zeigt alle Gruppen an, für welche eine Mitgliedschaft besteht
- [/groups/{group_id}](#/User/api_v1_groups_read) zeigt Informationen zu einer spezifischen Gruppe an
