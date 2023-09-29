"use strict";

const ENV_MAP = {
  kt_bern: "be",
  kt_schwyz: "sz",
  kt_uri: "ur",
  kt_gr: "gr",
  kt_so: "so",
};

const ENVS = Object.values(ENV_MAP);
const ENV = ENV_MAP[process.env.APPLICATION] || ENVS[0];

module.exports = {
  name: require("./package").name,

  included(...args) {
    this._super.included.apply(this, args);

    this.import("node_modules/proj4/dist/proj4.js");
    this.import("node_modules/proj4leaflet/src/proj4leaflet.js");
  },

  options: {
    "@embroider/macros": {
      // This config is only used for feature flags (when code
      // should be stripped during build time) and environment-specific
      // settings. Other config should go into `ember-ebau-core/addon/config`.
      setOwnConfig: {
        // basic setup
        application: ENV,
        isBE: ENV === "be",
        isSZ: ENV === "sz",
        isUR: ENV === "ur",
        isGR: ENV === "gr",
        isSO: ENV === "so",
        // environment-specific settings
        portalUrl: process.env.PORTAL_URL || "http://ebau-portal.local",
        soGisUrl: process.env.SO_GIS_URL || "https://geo-i.so.ch",
        // feature flags
        hasBuildingControl: ENV === "be",
        excelExportEnabled: ["be", "sz"].includes(ENV),
        showCreatePaperButton: ["be", "gr"].includes(ENV),
        showMergeAndSaveButton: ENV !== "gr",
      },
    },
  },
};
