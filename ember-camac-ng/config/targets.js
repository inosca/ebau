"use strict";

const isProduction = process.env.EMBER_ENV === "production";

const browsers = isProduction
  ? [
      "last 2 Chrome versions",
      "last 2 Firefox versions",
      "last 2 Safari versions",
      "ie 11",
    ]
  : ["last 1 Chrome versions", "last 1 Firefox versions"];

module.exports = { browsers };
