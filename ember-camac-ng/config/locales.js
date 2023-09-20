"use strict";

const LOCALES_MAP = {
  kt_bern: ["de", "fr"],
  kt_schwyz: ["de"],
  kt_uri: ["de"],
  kt_gr: ["de", "it"],
};

module.exports = LOCALES_MAP[process.env.APPLICATION || "kt_bern"];
