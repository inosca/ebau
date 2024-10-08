"use strict";

const path = require("path");

module.exports = function (environment) {
  return {
    clientAllowedKeys: [
      "APPLICATION",
      "APP_ENV",
      "KEYCLOAK_HOST",
      "KEYCLOAK_REALM",
      "PORTAL_URL",
    ],
    path: path.join(path.dirname(__dirname), "../.env"),
    enabled: environment !== "production",
  };
};
