"use strict";

const path = require("path");

module.exports = function () {
  return {
    clientAllowedKeys: ["APPLICATION", "APP_ENV"],
    path: path.join(path.dirname(__dirname), "../.env"),
  };
};
