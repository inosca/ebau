# Keycloak Theming

## Production build

We're using a multi-stage Docker build that

1. Builds the themes JAR file using a generic Java container and Maven.
2. Build keycloak, including the themes JAR file
3. Runs keycloak containing the build artifacts

You can also build the themes locally by running `make build-keycloak-themes`.

## Development setup

In the development setup, we're also mounting the theme source code as volume (`<canton>-dev`) and start the containers with the necessary flags to disable caching. Since those `-dev` themes are already configured in the dumped keycloak config, you should be able to make changes to the themes and directly see their effect in the browser.

## Styling

The theme for Kt. UR is based on UIkit, which is built using SASS:

```
cd themes
yarn
yarn build # builds css once
yarn watch # builds css on file change
```

## Message of the day (MOTD) (only Kt. UR and Kt. GR)

You can show a notice on the login screen by setting the `HTML Display name` property of your realm under Configure > Realm Settings.

## Custom authenticator

We're implementing two internal SPIs to support 2FA auth via SMS:

- required action: Used in the registration process for first setup
- authenticator: The actual 2FA logic during login

### Debugging

It is possible to debug the SPI code using VScode with the following settings on the `keycloak` container:

```yaml
environment:
  - DEBUG_MODE=true
  - DEBUG_PORT="*:8787"
ports:
  - 8080:8080
  - 8787:8787
command: [
    ...
    "--debug",
  ]
```

## Kt. Bern theme changes

Besides the actual theme changes the following changes are necessary to deliver
a new keycloak theme for usage in the Kt. BE setup (test/prod).

### Requirements (as of 2024-12):
- JAR file with the name format `keycloak-<theme-name>-theme-<theme-version>.jar`
- `keycloak-themes.json` contains the theme name with it's version
- The theme directory includes the theme version

### Versioning the theme
The following modifications should be applied (and committed to the upstream repository).

- Bump the version tag in `keycloak/themes/pom.xml`
  ```xml
  <version>x.x.x</version>
  ```
- Update the theme name with the new version number in
 `keycloak/themes/src/main/resources/META-INF/keycloak-themes.json`

  ```json
    "themes": [
      {
        "name": "ebau-be-x.x.x",
        "types": ["login"]
      }
    ]
  ```
- Rename the theme directory `keycloak/themes/src/main/resources/theme/ebau-be-x.x.x`
with the new version number. The directory should include all the theme changes.
- Update the path to the theme directory (`keycloak/themes/src/main/resources/theme/ebau-be-x.x.x`)
in the compose files.

### Renaming the JAR file (do not upstream)
- Rename the generated JAR file by applying the name changes to the `keycloak/themes/pom.xml`
  ```xml
  <name>keycloak-ebau-be-theme-x.x.x</name>
  <finalName>keycloak-ebau-be-theme-x.x.x</finalName>
  ```
- Update the JAR file path in `keycloak/Dockerfile` (e.g. copy paths).

### Removing unneeded themes (do not upstream)
- Remove the other canton themes in the `keycloak/themes/src/main/resources/META-INF/keycloak-themes.json`
file and from the `keycloak/themes/src/main/resources/theme/` directory.

### Deliverables
Build the keycloak theme by building the keycloak container and deliver the generated JAR
under the path `/opt/keycloak/providers` from the container.
