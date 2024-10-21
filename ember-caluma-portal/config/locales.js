"use strict";

const LOCALES_MAP = {
  demo: ["de", "fr"],
  kt_bern: ["de", "fr"],
  kt_uri: ["de"],
  kt_gr: ["de"],
  kt_so: ["de"],
  kt_ag: ["de"],
};

module.exports =
  process.env.LOCALES?.split(",") ||
  LOCALES_MAP[process.env.APPLICATION || "kt_bern"];
