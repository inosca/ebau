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

