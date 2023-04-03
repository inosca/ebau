# keycloak-theme-kanton-uri

Keycloak-Theme für den Kanton Uri.

## Versionierung

Das Projekt wird via Maven über das `pom.xml` versioniert (Element `version`).

## Docker-Image

Das Theme wird aktuell in ein vom offiziellen Keycloak-Image abgeleitetem Docker-Image paketiert.
Dabei wird folgendes Schema für die Tags verwendet:

```
${KEYCLOAK_VERSION}_theme-${THEME_VERSION}
```

Beispiel:

```
21.0.2_theme-v0.3.12
```

## Entwicklung - Maven und Versionierung

Wir verwenden den [Maven-Wrapper von takari](https://github.com/takari/maven-wrapper) um mit Maven das Docker Image zu bauen:

```sh
./mvnw install
```

## Entwicklung - Keycloak

Folgender Befehl startet einen Keycloak Docker-Container und mountet das Theme im dafür vorgesehenen Verzeichnis:

```bash
docker run \
  -d \
  -v $(pwd)/src/main/resources/theme/kanton-uri:/opt/keycloak/themes/kanton-uri \
  -e KEYCLOAK_ADMIN=admin \
  -e KEYCLOAK_ADMIN_PASSWORD=camac \
  -p 8080:8080 \
  quay.io/keycloak/keycloak:21.0.2 \
  start-dev

```

Danach kann man sich unter `http://localhost:8080/admin` als Admin einloggen und das Theme ändern. Wichtig: Es muss mindestens ein Identity Provider konfiguriert werden, damit das Theme die Login-Maske anzeigt!

Wenn am Theme entwickelt wird, muss evtl. der Theme Cache deaktiviert werden. Siehe https://www.keycloak.org/docs/latest/server_development/#creating-a-theme für Details.

## Entwicklung - Styling

Das Theme basiert auf UIkit, welches mit SASS angepasst wird.

```
yarn
yarn build # builds css once
yarn build # builds css on file change
```

