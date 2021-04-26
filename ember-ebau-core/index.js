"use strict";

module.exports = {
  name: require("./package").name,

  included(...args) {
    this._super.included.apply(this, args);

    this.import("node_modules/proj4/dist/proj4.js");
    this.import("node_modules/proj4leaflet/src/proj4leaflet.js");
  },
};
