"use strict";

const EmberApp = require("ember-cli/lib/broccoli/ember-app");

module.exports = function(defaults) {
  const app = new EmberApp(defaults, {
    // always enable sourcemaps
    sourcemaps: { enabled: true },
    // add configuration to source code instead of the meta tag
    storeConfigInMeta: false,
    // disable fingerprinting completely
    SRI: { enabled: false },
    fingerprint: { enabled: false }
  });

  app.import("node_modules/proj4/dist/proj4.js");
  app.import("node_modules/proj4leaflet/src/proj4leaflet.js");
  app.import("node_modules/moment/locale/de.js");
  app.import("node_modules/moment/locale/fr.js");

  return app.toTree();
};
