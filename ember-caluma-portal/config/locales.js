"use strict";

const LOCALES_MAP = {
  kt_gr: ["de", "it", "rm"],
  demo: ["de", "fr"],
  kt_bern: ["de", "fr"],
  kt_uri: ["de"],
};

module.exports = LOCALES_MAP[process.env.APPLICATION || "kt_bern"];
