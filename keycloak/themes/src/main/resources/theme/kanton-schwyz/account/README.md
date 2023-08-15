# Account theme details

## Source of the original theme

We extend our theme from the keycloak.v2 core theme. Since version 2 the
account theme is handled through a own react app. As a low effort approach we
decided to copy the core app and adjust the CSS to fit the CI of the customer.

The original account app can be found here:
https://github.com/keycloak/keycloak/tree/main/themes/src/main/resources/theme/keycloak.v2/account

## Changes done by Adfinis

Changed `theme.properties` variables as followed:
* parent=keycloak.v2
* logoUrl=./#/personal-info

Replaced `resources/public/logo.svg` and `resources/public/favicon.ico`.

Added Adfinis specific CSS rules to `resources/public/layout.css`.
