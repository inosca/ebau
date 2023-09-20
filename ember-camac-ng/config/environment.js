"use strict";

module.exports = function (environment) {
  const ENV = {
    modulePrefix: "camac-ng",
    environment,
    appEnv: process.env.APP_ENV || "development",
    rootURL: "/",
    locationType: "hash",
    historySupportMiddleware: true,
    apollo: {
      apiURL: "/graphql/",
    },
    EmberENV: {
      FEATURES: {
        // Here you can enable experimental features on an ember canary build
        // e.g. EMBER_NATIVE_DECORATOR_SUPPORT: true
      },
    },
    APP: {
      rootElement: "#ember-camac-ng",
    },
    "changeset-validations": { rawOutput: true },
  };

  if (environment === "test") {
    // Testem prefers this...
    ENV.locationType = "none";

    // keep test console output quieter
    ENV.APP.LOG_ACTIVE_GENERATION = false;
    ENV.APP.LOG_VIEW_LOOKUPS = false;

    ENV.APP.rootElement = "#ember-testing";
    ENV.APP.autoboot = false;
  }

  if (environment === "production") {
    // here you can enable a production-specific feature
  }

  ENV.routerScroll = { targetElement: ENV.APP.rootElement };

  return ENV;
};
