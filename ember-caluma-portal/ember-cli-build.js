"use strict";

const stew = require("broccoli-stew");
const EmberApp = require("ember-cli/lib/broccoli/ember-app");

const ENV_MAP = {
  kt_gr: "gr",
  kt_bern: "be",
  kt_schwyz: "sz",
  kt_uri: "ur",
  kt_so: "so",
  demo: "demo",
};

const ENVS = Object.values(ENV_MAP);
const ENV = ENV_MAP[process.env.APPLICATION] || ENVS[0];
const UNUSED_ENVS = ENVS.filter((e) => e !== ENV).join("|");

module.exports = function (defaults) {
  const app = new EmberApp(defaults, {
    storeConfigInMeta: !["so"].includes(ENV),
    "@embroider/macros": {
      setOwnConfig: {
        application: ENV,
        enableFaq: ENV === "be",
        enableSupport: ["be", "ur", "gr"].includes(ENV),
        enableInstanceSupport: ["be", "gr"].includes(ENV),
        enableModificationConfirm: ENV === "be",
        enableInstanceActionDescription: ENV !== "so",
        instancePaperFilterDefault: ENV === "ur",
        showProfileLink: ENV === "gr",
      },
      setConfig: {
        "@ember-data/store": {
          polyfillUUID: true,
        },
      },
    },
    "localized-model": {
      sanitizeLocale: true,
    },
    "ember-simple-auth": {
      useSessionSetupMethod: true,
    },
    fingerprint: {
      extensions: ["js", "css", "map"],
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

  app.trees.styles = stew.rm(
    stew.rename(app.trees.styles, `-${ENV}.scss`, ".scss"),
    `*/*-{${UNUSED_ENVS}}.scss`,
  );

  app.trees.app = stew.rm(
    stew.rename(app.trees.app, `-${ENV}.hbs`, ".hbs"),
    `*/*-{${UNUSED_ENVS}}.hbs`,
  );

  app.trees.public = stew.rm(
    stew.rename(app.trees.public, `-${ENV}.ico`, ".ico"),
    `*/*-{${UNUSED_ENVS}}.ico`,
  );

  return app.toTree();
};
