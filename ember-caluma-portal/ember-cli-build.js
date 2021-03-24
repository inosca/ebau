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
    sourcemaps: {
      enabled: true,
      extensions: ["js"],
    },
    "ember-cli-babel": {
      includePolyfill: true,
    },
  });

  // intersection observer polyfill
  app.import("node_modules/intersection-observer/intersection-observer.js");

  const unusedEnvs = ENVS.filter((e) => e !== ENV);

  const stylesTree = stew.rm(
    stew.rename(app.trees.styles, `-${ENV}.scss`, ".scss"),
    `*/*-{${unusedEnvs.join("|")}}.scss`
  );
  app.trees.styles = stylesTree;

  const appTree = stew.rm(
    stew.rename(app.trees.app, `-${ENV}.hbs`, ".hbs"),
    `*/*-{${unusedEnvs.join("|")}}.hbs`
  );
  app.trees.app = appTree;

  return app.toTree();
};
