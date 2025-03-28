"use strict";

module.exports = function (environment) {
  const app = process.env.APPLICATION;

  /**
   * Build time configuration
   *
   * This code is used in two different scenarios:
   *
   * 1. When running the frontend locally, the env vars are usually not set, so
   *    the defaults apply.
   * 2. When running the frontend in a container, the env vars are set as build
   *    ARGs to a static string (e.g. "$KEYCLOAK_HOST") which is replaced with
   *    the value of the env var at _runtime_ by the entrypoint script. Keep in
   *    mind that when this script is running (at build time), the actual value
   *    of the env var is not known!
   *
   * See docs/config-mgmt.md for more information.
   */
  const {
    // Defaults only apply when run with ember dev server or when the image is
    // not built with KEYCLOAK_* build arguments
    KEYCLOAK_HOST = "http://ebau-keycloak.local",
    KEYCLOAK_BASE_PATH = "auth/",
    KEYCLOAK_REALM = app === "kt_uri" ? "urec" : "ebau",
    KEYCLOAK_CLIENT = "camac",
    KEYCLOAK_SCOPES = "openid",
  } = process.env;

  // Since we don't know the actual value of the env var at build time, we can't
  // strip or add any slashes here. KEYCLOAK_HOST and KEYCLOAK_BASE_PATH should
  // both have a trailing slash.
  const oidcUrl = `${KEYCLOAK_HOST}/${KEYCLOAK_BASE_PATH}realms/${KEYCLOAK_REALM}`;

  const ENV = {
    modulePrefix: "ebau",
    environment,
    rootURL: "/",
    locationType: "history",
    "changeset-validations": { rawOutput: true },
    "ember-simple-auth-oidc": {
      host: `${oidcUrl}/protocol/openid-connect`,
      clientId: KEYCLOAK_CLIENT,
      scope: KEYCLOAK_SCOPES,
      authEndpoint: "/auth",
      tokenEndpoint: "/token",
      endSessionEndpoint: "/logout",
      userinfoEndpoint: "/userinfo",
      afterLogoutUri: "/login",
      loginHintName: "kc_idp_hint",
      enablePkce: true,
    },
    "ember-caluma": {
      FLATPICKR_DATE_FORMAT: {
        de: "d.m.Y",
        fr: "d.m.Y",
        it: "d.m.Y",
        en: "m/d/Y",
      },
      FLATPICKR_DATE_FORMAT_DEFAULT: "d.m.Y",
      USE_MANDATORY_ASTERISK: ["kt_ag", "kt_gr"].includes(app),
    },
    apollo: {
      apiURL: "/graphql/",
    },
    EmberENV: {
      EXTEND_PROTOTYPES: false,
      FEATURES: {
        // Here you can enable experimental features on an ember canary build
        // e.g. EMBER_NATIVE_DECORATOR_SUPPORT: true
      },
    },
    APP: {
      // Here you can pass flags/options to your application instance
      // when it is created
    },
  };

  if (environment === "development") {
    // ENV.APP.LOG_RESOLVER = true;
    // ENV.APP.LOG_ACTIVE_GENERATION = true;
    // ENV.APP.LOG_TRANSITIONS = true;
    // ENV.APP.LOG_TRANSITIONS_INTERNAL = true;
    // ENV.APP.LOG_VIEW_LOOKUPS = true;
  }

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

  return ENV;
};
