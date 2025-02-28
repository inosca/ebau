"use strict";

module.exports = function (environment) {
  const oidcHost = process.env.KEYCLOAK_HOST ?? "http://ebau-keycloak.local";
  const oidcBasePath = process.env.KEYCLOAK_BASE_PATH ?? "auth";
  const oidcRealm =
    process.env.KEYCLOAK_REALM ??
    (process.env.APPLICATION === "kt_uri" ? "urec" : "ebau");
  const oidcClientId = process.env.KEYCLOAK_CLIENT ?? "camac";
  const oidcScopes = process.env.KEYCLOAK_SCOPES ?? "oidc";

  function trailingSlash(url) {
    if (!url) {
      return "";
    }
    return url.replace(/\/?$/, "/");
  }
  const oidcUrl = `${trailingSlash(oidcHost)}${trailingSlash(oidcBasePath)}realms/${oidcRealm}`;

  const ENV = {
    modulePrefix: "ebau",
    environment,
    rootURL: "/",
    locationType: "history",
    "changeset-validations": { rawOutput: true },
    "ember-simple-auth-oidc": {
      host: `${oidcUrl}/protocol/openid-connect`,
      clientId: oidcClientId,
      scope: oidcScopes,
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
      USE_MANDATORY_ASTERISK: ["kt_ag", "kt_gr"].includes(
        process.env.APPLICATION,
      ),
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
