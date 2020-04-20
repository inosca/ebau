"use strict";

module.exports = function(environment) {
  let oidcHost =
    process.env.KEYCLOAK_URL ||
    "http://camac-ng-keycloak.local/auth/realms/ebau/protocol/openid-connect";

  let ENV = {
    modulePrefix: "citizen-portal",
    environment,
    rootURL: "/",
    locationType: "auto",
    oidcHost,
    profileURL: oidcHost.replace("protocol/openid-connect", "account"),
    EmberENV: {
      FEATURES: {
        // Here you can enable experimental features on an ember canary build
        // e.g. 'with-controller': true
      },
      EXTEND_PROTOTYPES: {
        // Prevent Ember Data from overriding Date.parse.
        Date: false
      }
    },

    APP: {
      // special attachment section mapping
      attachmentSections: { applicant: "1", readOnly: "9", publication: "4" },

      // array of active municipality names,
      // used in submit and camac-property-selector
      municipalityNames: [],

      gisHost: "map-t.geo.sz.ch",

      // Form location mapping in order of definition
      // konzession-fur-wasserentnahme = Amt für Wasserbau
      // projektgenehmigungsgesuch-gemass-ss15-strag = Tiefbauamt
      // anlassbewilligungen-verkehrsbewilligungen = Kantons Polizei
      formLocations: {
        7: "Amt für Wasserbau",
        9: "Tiefbauamt des Kantons Schwyz",
        10: "Kantonspolizei Schwyz"
      }
    },

    exportApplicationGlobal: true,

    "ember-simple-auth-oidc": {
      host: oidcHost.replace(/\/$/, ""),
      clientId: "portal",
      authEndpoint: "/auth",
      tokenEndpoint: "/token",
      userinfoEndpoint: "/userinfo",
      endSessionEndpoint: "/logout",
      afterLogoutUri: "/"
    },

    "ember-validated-form": {
      css: {
        group: "uk-margin",
        control: "uk-input",
        label: "uk-form-label uk-text-bolder",
        checkbox: "uk-checkbox",
        radio: "uk-radio",
        button: "uk-button uk-button-default",
        submit: "uk-button uk-button-primary"
      }
    },

    moment: {
      includeLocales: ["de-ch"]
    }
  };

  if (environment === "development") {
    // ENV.APP.LOG_RESOLVER = true;
    // ENV.APP.LOG_ACTIVE_GENERATION = true;
    // ENV.APP.LOG_TRANSITIONS = true;
    // ENV.APP.LOG_TRANSITIONS_INTERNAL = true;
    // ENV.APP.LOG_VIEW_LOOKUPS = true;
    ENV.APP.municipalityNames = [
      "Alpthal",
      "Altendorf",
      "Arth",
      "Einsiedeln",
      "Feusisberg",
      "Freienbach",
      "Galgenen",
      "Gersau",
      "Illgau",
      "Ingenbohl",
      "Innerthal",
      "Küssnacht",
      "Lachen",
      "Lauerz",
      "Morschach",
      "Muotathal",
      "Oberiberg",
      "Rechenburg",
      "Riemenstalden",
      "Rothenthurm",
      "Sattel",
      "Schwyz",
      "Schübelbach",
      "Steinen",
      "Steinerberg",
      "Tuggen",
      "Unteriberg",
      "Vorderthal",
      "Wangen",
      "Wollerau",
      "Amt für Wasserbau",
      "Tiefbauamt des Kantons Schwyz",
      "Kantonspolizei Schwyz"
    ];
  }

  if (environment === "test") {
    // Testem prefers this...
    ENV.locationType = "none";

    // keep test console output quieter
    ENV.APP.LOG_ACTIVE_GENERATION = false;
    ENV.APP.LOG_VIEW_LOOKUPS = false;

    ENV.APP.rootElement = "#ember-testing";
    ENV.APP.autoboot = false;

    ENV["ember-simple-auth-oidc"] = {
      authEndpoint: "/auth/realms/ebau/protocol/openid-connect/auth",
      tokenEndpoint: "/auth/realms/ebau/protocol/openid-connect/token",
      logoutEndpoint: "/auth/realms/ebau/protocol/openid-connect/logout"
    };
  }

  if (environment === "stage") {
    ENV["ember-cli-mirage"] = {
      enabled: process.env.EMBER_CLI_MIRAGE || false
    };

    ENV.APP.municipalityNames = [
      "Alpthal",
      "Altendorf",
      "Arth",
      "Einsiedeln",
      "Feusisberg",
      "Freienbach",
      "Galgenen",
      "Gersau",
      "Illgau",
      "Ingenbohl",
      "Innerthal",
      "Küssnacht",
      "Lachen",
      "Lauerz",
      "Morschach",
      "Muotathal",
      "Oberiberg",
      "Rechenburg",
      "Riemenstalden",
      "Rothenthurm",
      "Sattel",
      "Schwyz",
      "Schübelbach",
      "Steinen",
      "Steinerberg",
      "Tuggen",
      "Unteriberg",
      "Vorderthal",
      "Wangen",
      "Wollerau",
      "Amt für Wasserbau",
      "Tiefbauamt des Kantons Schwyz",
      "Kantonspolizei Schwyz"
    ];
  }

  if (environment === "production") {
    ENV["ember-cli-mirage"] = {
      enabled: process.env.EMBER_CLI_MIRAGE || false
    };

    ENV.APP.municipalityNames = [
      "Alpthal",
      "Galgenen",
      "Innerthal",
      "Lauerz",
      "Muotathal",
      "Oberiberg",
      "Riemenstalden",
      "Rothenthurm",
      "Steinen",
      "Steinerberg",
      "Amt für Wasserbau",
      "Tiefbauamt des Kantons Schwyz",
      "Kantonspolizei Schwyz"
    ];

    ENV.APP.gisHost = "map.geo.sz.ch";
  }

  return ENV;
};
