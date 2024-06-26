// copied from ember-caluma-portal
"use strict";

const LOCALES_MAP = {
  kt_gr: ["de", "it"],
  demo: ["de", "fr"],
  kt_bern: ["de", "fr"],
  kt_uri: ["de"],
  kt_schwyz: ["de"],
  kt_so: ["de"],
};

module.exports = LOCALES_MAP[process.env.APPLICATION || "demo"];
