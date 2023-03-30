# keycloak-theme eBau BE

Keycloak-Theme für eBau Kanton Bern.

Ein reines Umstylen des Standard-Themes ist bei dem Layout des Kantons sehr aufwändig, daher wird kein Umstyling
des bestehenden Themes durchgeführt, sondern die betroffenen Seiten (`login` und `login-update-profile`) komplett
überschrieben.

Keycloak verwendet dafür Freemarker-Templates mit fest definierten Namen. Siehe
`themes/src/main/resources/theme/base/login` im Keycloak git repository für alle Freemarker-Templates und die
vom Standard-Theme verwendeten Freemarker-Direktiven.

## Styles

Alle notwendigen Styles vom Layout des Kantons wurden übernommen und einige Styles überschrieben:

* `keycloak-images-overrides.css` überschreibt CSS-Rules, die Bilder referenzieren und ändert die background URL
  auf einen in Keycloak gültigen Pfad.
* `keycloak-sprite-overrides.css` überschreibt alle CSS-Rules, die die Kanton Bern sprites (Icons) referenzieren und
  ändert die background URL auf einen in Keycloak gültigen Pfad
* `keycloak-overrides.css` fügt diverse Regeln hinzu, damit das Layout funktioniert

## Packetierung als JAR

Für den Build wird eine lokale Java JDK benötigt.

```
./mvnw clean package -B
```

## Deployment des Themes

### Normale Installation auf einem System

Nach der Installation von Keycloak das JAR des Themes an einen temporären Ort ablegen, zum Beispiel
`/tmp/keycloak-theme-ebau-be.jar` und anschliessend das `jboss-cli.sh` wie folgt aufrufen:

```bash
jboss-cli.sh --command="module add \
                               --name=ch.linkyard.ebau.be.theme.keycloak-theme-ebau-be \
                               --resources=/tmp/keycloak-theme-ebau-be.jar"
```

Danach im `standalone.xml` das Subsystem `urn:jboss:domain:keycloak-server:1.1` suchen und im
`theme` Element folgendes hinzufügen:

```xml
<modules>
  <module>ch.linkyard.ebau.be.theme.keycloak-theme-ebau-be</module>
</modules>
```

## Entwicklung - Maven und Versionierung

Wir verwenden den [Maven-Wrapper von takari](https://github.com/takari/maven-wrapper) um Maven in das Projekt zu
integrieren (Start von Maven mit `mvnw` bzw. `mvnw.cmd`).

Das Projekt wird mit aus Git-Metainformationen mit dem
[jgitver-maven-plugin](https://github.com/jgitver/jgitver-maven-plugin) versioniert.

## Entwicklung - Keycloak

Zur Entwicklung des Themes, einen Keycloak Docker-Container starten und das Directory
`src/main/resources/theme/ebau-be` in den Docker-Container unter `/opt/jboss/keycloak/themes/ebau-be`
mounten:

```bash
docker run \
  -d \
  -v $(pwd)/src/main/resources/theme/ebau-be:/opt/jboss/keycloak/themes/ebau-be \
  -e KEYCLOAK_USER=admin \
  -e KEYCLOAK_PASSWORD=changeit \
  -p 8080:8080 \
  --name keycloak-theme-be \
  jboss/keycloak:16.1.0
```

Danach kann man sich unter `http://localhost:8080/auth` als Admin einloggen und das Theme ändern.

Das Theme-Caching von Keycloak deaktivieren, dazu im Container die Datei
`/opt/jboss/keycloak/standalone/configuration/standalone.xml` editieren und im `theme` Block:

* `staticMaxAge`: `-1`
* `cacheThemes`: `false`
* `cacheTemplates`: `false`

```xml
<theme>
    <staticMaxAge>-1</staticMaxAge>
    <cacheThemes>false</cacheThemes>
    <cacheTemplates>false</cacheTemplates>
</theme>
```

Anschliessend den Container neu starten.

Sollte das nicht funktionieren, kann das Caching auch [über jboss-cli deaktiviert werden](https://keycloakthemes.com/blog/how-to-turn-off-the-keycloak-theme-cache).

## Quirks

`.properties` files wie zum Beispiel die `messages_de.properties` für Internationalization müssen UTF-8 encoded werden, damit Java diese richtig darstellen und in die Template rendern kann.
`native2ascii -encoding UTF-8 messages_de.properties`
