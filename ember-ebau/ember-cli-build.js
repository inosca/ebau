"use strict";

const stew = require("broccoli-stew");
const EmberApp = require("ember-cli/lib/broccoli/ember-app");

const ENV_MAP = {
  kt_gr: "gr",
  kt_bern: "be",
  kt_schwyz: "sz",
  kt_uri: "ur",
  kt_so: "so",
};

const ENVS = Object.values(ENV_MAP);
const ENV = ENV_MAP[process.env.APPLICATION] || ENVS[0];
const UNUSED_ENVS = ENVS.filter((e) => e !== ENV).join("|");

module.exports = function (defaults) {
  const app = new EmberApp(defaults, {
    storeConfigInMeta: ENV !== "so",
    "localized-model": {
      sanitizeLocale: true,
    },
    "ember-simple-auth": {
      useSessionSetupMethod: true,
    },
    "@embroider/macros": {
      setConfig: {
        "@ember-data/store": {
          polyfillUUID: true,
        },
      },
      setOwnConfig: {
        application: ENV,
      },
    },
    fingerprint: {
      extensions: ["js", "css", "map"],
    },
  });

  app.trees.app = stew.rm(
    stew.rename(app.trees.app, `-${ENV}.js`, ".js"),
    `*/*-{${UNUSED_ENVS}}.js`,
  );

  app.trees.app = stew.rm(
    stew.rename(app.trees.app, `-${ENV}.hbs`, ".hbs"),
    `*/*-{${UNUSED_ENVS}}.hbs`,
  );

  app.trees.styles = stew.rm(
    stew.rename(app.trees.styles, `-${ENV}.scss`, ".scss"),
    `*/*-{${UNUSED_ENVS}}.scss`,
  );

  app.trees.public = stew.rm(
    stew.rename(app.trees.public, `-${ENV}.ico`, ".ico"),
    `*/*-{${UNUSED_ENVS}}.ico`,
  );

  return app.toTree();
};
