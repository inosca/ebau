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
      setOwnConfig: {
        application: ENV,
        hasBuildingControl: ENV === "be",
        isBE: ENV === "be",
        isSZ: ENV === "sz",
        isUR: ENV === "ur",
        isSO: ENV === "so",
        excelExportEnabled: ["be", "sz"].includes(ENV),
      },
    },
  },
};
