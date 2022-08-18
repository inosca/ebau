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
const UNUSED_ENVS = ENVS.filter((e) => e !== ENV).join("|");

module.exports = function (defaults) {
  const app = new EmberApp(defaults, {
    "ember-simple-auth": {
      useSessionSetupMethod: true,
    },
    fingerprint: {
      extensions: ["js", "css", "map"],
    },
    "@embroider/macros": {
      setOwnConfig: {
        application: ENV,
        isBE: ENV === "be",
        isSZ: ENV === "sz",
        isUR: ENV === "ur",
      },
    },
  });

  app.import("node_modules/proj4/dist/proj4.js");
  app.import("node_modules/proj4leaflet/src/proj4leaflet.js");

  app.trees.app = stew.rm(
    stew.rename(app.trees.app, `-${ENV}.js`, ".js"),
    `*/*-{${UNUSED_ENVS}}.js`
  );

  app.trees.app = stew.rm(
    stew.rename(app.trees.app, `-${ENV}.hbs`, ".hbs"),
    `*/*-{${UNUSED_ENVS}}.hbs`
  );

  app.trees.styles = stew.rm(
    stew.rename(app.trees.styles, `-${ENV}.scss`, ".scss"),
    `*/*-{${UNUSED_ENVS}}.scss`
  );

  return app.toTree();
};
