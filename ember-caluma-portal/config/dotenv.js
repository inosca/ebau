"use strict";

const path = require("path");

module.exports = function () {
  return {
    clientAllowedKeys: ["APPLICATION", "KEYCLOAK_HOST", "BE_GIS_URL"],
    path: path.join(path.dirname(__dirname), "../.env"),
  };
};
