"use strict";

const stew = require("broccoli-stew");
const EmberApp = require("ember-cli/lib/broccoli/ember-app");

const ENV_MAP = {
  kt_gr: "gr",
  kt_bern: "be",
  kt_schwyz: "sz",
  kt_uri: "ur",
  kt_so: "so",
  kt_ag: "ag",
};

const ENVS = Object.values(ENV_MAP);
const ENV = ENV_MAP[process.env.APPLICATION] || ENVS[0];
const UNUSED_ENVS = ENVS.filter((e) => e !== ENV).join("|");

module.exports = function (defaults) {
  const app = new EmberApp(defaults, {
    minifyCSS: {
      // https://github.com/clean-css/clean-css/issues/1280
      options: { level: { 1: { all: true, tidySelectors: false } } },
    },
    storeConfigInMeta: !["so", "ag"].includes(ENV),
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
    "ember-validated-form": {
      theme: "uikit",
    },
    babel: {
      plugins: [
        require.resolve("ember-concurrency/async-arrow-task-transform"),
      ],
    },
    // Disable striping of test selectors in production builds as babel would
    // fail. If we downgrade to v6 of ember-test-selectors it wouldn't work as
    // well as it doesn't support our babel version. TODO: Remove this when
    // https://github.com/mainmatter/ember-test-selectors/issues/1259 is fixed.
    "ember-test-selectors": {
      strip: false,
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
