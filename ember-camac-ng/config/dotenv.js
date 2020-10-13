"use strict";

const path = require("path");

module.exports = function(env) {
  return {
    enabled: env !== "production",
    clientAllowedKeys: ["APPLICATION"],
    path: path.join(path.dirname(__dirname), "../.env")
  };
};
