"use strict";

const path = require("path");

module.exports = function (environment) {
  return {
    clientAllowedKeys: [
      "APPLICATION",
      "KEYCLOAK_HOST",
      "PORTAL_URL",
      "SO_GIS_URL",
      "ENABLE_WATERMARK",
      "WATERMARK",
      "ALEXANDRIA_MANABI_ALLOWED_MIMETYPES",
      "LOCALES",
    ],
    path: path.join(path.dirname(__dirname), "../.env"),
    enabled: environment !== "production",
  };
};
