"use strict";

const path = require("path");

module.exports = function () {
  return {
    clientAllowedKeys: ["APPLICATION", "KEYCLOAK_HOST"],
    path: path.join(path.dirname(__dirname), "../.env"),
  };
};
