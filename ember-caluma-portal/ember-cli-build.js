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
    storeConfigInMeta: ENV !== "so",
    "@embroider/macros": {
      setOwnConfig: {
        application: ENV,
        enableFaq: ENV === "be",
        enableSupport: ["be", "ur", "gr"].includes(ENV),
        enableInstanceSupport: ENV === "be",
        enableModificationConfirm: ENV === "be",
        enableCommunications: ["be", "so"].includes(ENV),
        enableAdditionalDemand: ["gr", "so"].includes(ENV),
        enableInstanceActionDescription: ENV !== "so",
        instancePaperFilterDefault: ENV === "ur",
        showProfileLink: ENV === "gr",
        eGovPortalURL: process.env.EGOV_PORTAL_URL ?? "https://my-t.so.ch",
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
