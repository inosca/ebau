"use strict";

const LOCALES_MAP = {
  demo: ["de", "fr"],
  kt_bern: ["de", "fr"],
  kt_uri: ["de"],
  kt_gr: ["de", "fr", "rm"],
};

module.exports = LOCALES_MAP[process.env.APPLICATION || "kt_bern"];
