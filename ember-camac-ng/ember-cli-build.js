"use strict";

const stew = require("broccoli-stew");
const EmberApp = require("ember-cli/lib/broccoli/ember-app");

const ENV_MAP = {
  kt_bern: "be",
  kt_schwyz: "sz",
  kt_uri: "ur",
};

const ENVS = Object.values(ENV_MAP);
const ENV = ENV_MAP[process.env.APPLICATION] || ENVS[0];

module.exports = function (defaults) {
  const app = new EmberApp(defaults, {
    // always enable sourcemaps
    sourcemaps: { enabled: true },
    // add configuration to source code instead of the meta tag
    storeConfigInMeta: false,
    // disable fingerprinting completely
    SRI: { enabled: false },
    fingerprint: { enabled: false },
  });

  app.import("node_modules/proj4/dist/proj4.js");
  app.import("node_modules/proj4leaflet/src/proj4leaflet.js");

  const unusedEnvs = ENVS.filter((e) => e !== ENV);

  const stylesTree = stew.rm(
    stew.rename(app.trees.styles, `-${ENV}.scss`, ".scss"),
    `*/*-{${unusedEnvs.join("|")}}.scss`
  );

  app.trees.styles = stylesTree;

  return app.toTree();
};
