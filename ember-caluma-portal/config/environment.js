"use strict";

module.exports = function(environment) {
  const ENV = {
    modulePrefix: "ember-caluma-portal",
    environment,
    rootURL: "/",
    locationType: "auto",
    historySupportMiddleware: true,
    "ember-simple-auth-oidc": {
      host:
        "http://camac-ng-keycloak.local/auth/realms/ebau/protocol/openid-connect",
      clientId: "portal",
      authEndpoint: "/auth",
      tokenEndpoint: "/token",
      endSessionEndpoint: "/logout",
      userinfoEndpoint: "/userinfo",
      afterLogoutUri: "/login",
      forwardParams: ["kc_idp_hint"]
    },
    apollo: {
      apiURL: "/graphql/"
    },
    EmberENV: {
      FEATURES: {
        // Here you can enable experimental features on an ember canary build
        // e.g. EMBER_NATIVE_DECORATOR_SUPPORT: true
      },
      EXTEND_PROTOTYPES: {
        // Prevent Ember Data from overriding Date.parse.
        Date: false
      }
    },

    APP: {
      // Here you can pass flags/options to your application instance
      // when it is created
    },
    moment: {
      includeLocales: ["de", "fr"]
    },

    languages: ["de", "fr"],
    fallbackLanguage: "de",

    ebau: {
      internalURL: "http://camac-ng.local",
      claims: {
        notificationTemplateId: 32
      },
      attachments: {
        allowedMimetypes: ["image/png", "image/jpeg", "application/pdf"],
        buckets: [
          "dokument-grundstucksangaben",
          "dokument-gutachten-nachweise-begrundungen",
          "dokument-projektplane-projektbeschrieb",
          "dokument-weitere-gesuchsunterlagen"
        ]
      },
      supportGroups: [10000],
      selectableGroups: {
        roles: [
          3, // Leitung Leitbehörde
          5, // Leitung Baukontrolle
          20004, // Sachbearbeiter Leitbehörde
          20005, // Sachbearbeiter Baukontrolle
          10000 // System-Betrieb
        ]
      },
      paperInstances: {
        allowedGroups: {
          roles: [
            3, // Leitung Leitbehörde
            20004 // Sachbearbeiter Leitbehörde
          ],
          serviceGroups: [
            2, // Gemeinde
            20000 // Regierungsstatthalteramt
          ]
        }
      },
      instanceStates: {
        new: 1,
        rejected: 10000,
        archived: 20009,
        inCorrection: 20007,
        finished: 120000
      }
    }
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
