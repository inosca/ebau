"use strict";

const path = require("path");

module.exports = function () {
  return {
    clientAllowedKeys: [
      "APPLICATION",
      "KEYCLOAK_HOST",
      "KEYCLOAK_REALM",
      "BE_GIS_URL",
      "SO_GIS_URL",
      "INTERNAL_URL",
      "EGOV_PORTAL_URL",
      "EGOV_PRESTATION_PATH",
      "ENABLE_TOKEN_EXCHANGE",
      "ENABLE_WATERMARK",
      "WATERMARK",
    ],
    path: path.join(path.dirname(__dirname), "../.env"),
  };
};
