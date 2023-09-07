"use strict";

const path = require("path");

module.exports = function () {
  return {
    clientAllowedKeys: [
      "APPLICATION",
      "KEYCLOAK_HOST",
      "BE_GIS_URL",
      "SO_GIS_URL",
      "INTERNAL_URL",
      "EGOV_PORTAL_URL",
    ],
    path: path.join(path.dirname(__dirname), "../.env"),
  };
};
