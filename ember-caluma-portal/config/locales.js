"use strict";

const LOCALES_MAP = {
  demo: ["de", "fr"],
  kt_bern: ["de", "fr"],
  kt_uri: ["de"],
};

module.exports = LOCALES_MAP[process.env.APPLICATION || "kt_bern"];
