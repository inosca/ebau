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
    "@embroider/macros": {
      setOwnConfig: {
        application: ENV,
        enableFaq: ENV === "be",
        enableInstanceSupport: ENV === "be",
        enablePublicationForm: ENV === "be",
        enablePublicationEndDate: ENV === "ur",
        enableModificationConfirm: ENV === "be",
        enableCommunications: ["be", "so"].includes(ENV),
        instancePaperFilterDefault: ENV === "ur",
        showProfileLink: ["gr", "so"].includes(ENV),
        documentBackend: ENV === "gr" ? "alexandria" : "camac",
      },
      setConfig: {
        "@ember-data/store": {
          // https://github.com/emberjs/data/pull/8109
          polyfillUUID: true,
        },
      },
    },
    "ember-simple-auth": {
      useSessionSetupMethod: true,
    },
    fingerprint: {
      extensions: ["js", "css", "map"],
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
