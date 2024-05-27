"use strict";

const path = require("path");

module.exports = function () {
  return {
    clientAllowedKeys: [
      "APPLICATION",
      "APP_ENV",
      "KEYCLOAK_HOST",
      "PORTAL_URL",
    ],
    path: path.join(path.dirname(__dirname), "../.env"),
  };
};
