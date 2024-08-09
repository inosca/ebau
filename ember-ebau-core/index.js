"use strict";

const ENV_MAP = {
  kt_bern: "be",
  kt_schwyz: "sz",
  kt_uri: "ur",
  kt_gr: "gr",
  kt_so: "so",
  test: "test",
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
        enableWatermark: process.env.ENABLE_WATERMARK ?? false,
        watermark: process.env.WATERMARK ?? "dev",
        allowedWebDAVMimeTypes:
          process.env.ALEXANDRIA_MANABI_ALLOWED_MIMETYPES ??
          "application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        // feature flags
        hasBuildingControl: ENV === "be",
        useInstanceService: ENV !== "sz",
        // token exchange (this is not a regular feature flag because it differs
        // per environment in Kt. SO)
        enableTokenExchange: process.env.ENABLE_TOKEN_EXCHANGE ?? false,
        eGovPortalURL: process.env.EGOV_PORTAL_URL ?? "http://egov.local",
        eGovPrestationPath: process.env.EGOV_PRESTATION_PATH ?? "/prestation/1",
      },
    },
    babel: {
      plugins: [
        require.resolve("ember-concurrency/async-arrow-task-transform"),
      ],
    },
  },
};
