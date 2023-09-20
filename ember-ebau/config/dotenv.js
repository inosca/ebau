"use strict";

const path = require("path");

module.exports = function () {
  return {
    clientAllowedKeys: [
      "APPLICATION",
      "KEYCLOAK_HOST",
      "PORTAL_URL",
      "SO_GIS_URL",
    ],
    path: path.join(path.dirname(__dirname), "../.env"),
  };
};
