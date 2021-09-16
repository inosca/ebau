"use strict";

module.exports = function (environment) {
  const oidcHost =
    process.env.KEYCLOAK_URL ||
    "http://camac-ng-keycloak.local/auth/realms/ebau/protocol/openid-connect";

  const ENV = {
    modulePrefix: "citizen-portal",
    environment,
    rootURL: "/",
    locationType: "auto",
    oidcHost,
    profileURL: oidcHost.replace("protocol/openid-connect", "account"),
    apollo: {
      apiURL: "/graphql/",
    },
    EmberENV: {
      FEATURES: {
        // Here you can enable experimental features on an ember canary build
        // e.g. EMBER_NATIVE_DECORATOR_SUPPORT: true
      },
      EXTEND_PROTOTYPES: {
        // Prevent Ember Data from overriding Date.parse.
        Date: false,
      },
    },

    APP: {
      // special attachment section mapping
      attachmentSections: { applicant: "1", readOnly: "9", publication: "4" },

      // array of active municipality names,
      // used in submit and camac-property-selector
      municipalityNames: [],

      gisHost: "map-t.geo.sz.ch",

      // Form location mapping in order of definition
      // konzession-fur-wasserentnahme = Amt für Gewässer
      // anlassbewilligungen-verkehrsbewilligungen = Kantons Polizei
      // plangenehmigungsgesuch astra = Tiefbauamt
      // plangenehmigungsgesuch esti = Energiefachstelle
      // plangenehmigungsgesuch bav = Amt für Öffentlichenverkehr
      // plangenehmigungsgesuch vbs = Raumentwicklung
      // projektgenehmigungsgesuch-gemass-ss15-strag bezirk = Bezirksfachstelle
      // projektgenehmigungsgesuch-gemass-ss15-strag kanton = Tiefbauamt
      formLocations: {
        "14": "Amt für Gewässer",
        "17": "Kantonspolizei Schwyz",
        "15-astra": "Tiefbauamt des Kantons Schwyz",
        "15-esti": "Eidg. Starkstrominspektorat",
        "15-bavs": "Verkehrsamt Schwyz",
        "15-bavb": "Amt für öffentlichen Verkehr",
        "15-vbs": "Amt für Raumentwicklung",
        "15-bazl": "Amt für Raumentwicklung",
        "15-uebrige": "Amt für Raumentwicklung",
        "16-district": "district",
        "16-canton": "Tiefbauamt des Kantons Schwyz",
      },

      // Mapping used for identifying the district of a given municipality
      // used for form location 16-district
      districtMapping: {
        Einsiedeln: "Bezirk Einsiedeln",
        Gersau: "Bezirk Gersau",
        Küssnacht: "Bezirk Küssnacht",
        Feusisberg: "Bezirk Höfe",
        Freienbach: "Bezirk Höfe",
        Wollerau: "Bezirk Höfe",
        Altendorf: "Bezirk March",
        Galgenen: "Bezirk March",
        Innerthal: "Bezirk March",
        Lachen: "Bezirk March",
        Reichenburg: "Bezirk March",
        Schübelbach: "Bezirk March",
        Tuggen: "Bezirk March",
        Vorderthal: "Bezirk March",
        Wangen: "Bezirk March",
        Alpthal: "Bezirk Schwyz",
        Arth: "Bezirk Schwyz",
        Illgau: "Bezirk Schwyz",
        Ingenbohl: "Bezirk Schwyz",
        Lauerz: "Bezirk Schwyz",
        Morschach: "Bezirk Schwyz",
        Muotathal: "Bezirk Schwyz",
        Oberiberg: "Bezirk Schwyz",
        Riemenstalden: "Bezirk Schwyz",
        Rothenthrum: "Bezirk Schwyz",
        Sattel: "Bezirk Schwyz",
        Schwyz: "Bezirk Schwyz",
        Steinen: "Bezirk Schwyz",
        Steinerberg: "Bezirk Schwyz",
        Unteriberg: "Bezirk Schwyz",
      },
    },

    exportApplicationGlobal: true,

    "ember-simple-auth-oidc": {
      host: oidcHost.replace(/\/$/, ""),
      clientId: "portal",
      authEndpoint: "/auth",
      tokenEndpoint: "/token",
      userinfoEndpoint: "/userinfo",
      endSessionEndpoint: "/logout",
      afterLogoutUri: "/",
    },

    "ember-validated-form": {
      css: {
        group: "uk-margin",
        control: "uk-input",
        label: "uk-form-label uk-text-bolder",
        checkbox: "uk-checkbox",
        radio: "uk-radio",
        button: "uk-button uk-button-default",
        submit: "uk-button uk-button-primary",
      },
    },

    moment: {
      includeLocales: ["de-ch"],
    },
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
      "Amt für Gewässer",
      "Tiefbauamt des Kantons Schwyz",
      "Kantonspolizei Schwyz",
      "Eidg. Starkstrominspektorat",
      "Amt für öffentlichen Verkehr",
      "Amt für Raumentwicklung",
      "Verkehrsamt Schwyz",
      "Bezirk Einsiedeln",
      "Bezirk Gersau",
      "Bezirk Küssnacht",
      "Bezirk Höfe",
      "Bezirk March",
      "Bezirk Schwyz",
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
      logoutEndpoint: "/auth/realms/ebau/protocol/openid-connect/logout",
    };
  }

  if (environment === "stage") {
    ENV["ember-cli-mirage"] = {
      enabled: process.env.EMBER_CLI_MIRAGE || false,
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
      "Reichenburg",
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
      "Amt für Gewässer",
      "Tiefbauamt des Kantons Schwyz",
      "Kantonspolizei Schwyz",
      "Eidg. Starkstrominspektorat",
      "Amt für öffentlichen Verkehr",
      "Amt für Raumentwicklung",
      "Verkehrsamt Schwyz",
      "Bezirk Einsiedeln",
      "Bezirk Gersau",
      "Bezirk Küssnacht",
      "Bezirk Höfe",
      "Bezirk March",
      "Bezirk Schwyz",
    ];
  }

  if (environment === "production") {
    ENV["ember-cli-mirage"] = {
      enabled: process.env.EMBER_CLI_MIRAGE || false,
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
      "Amt für Gewässer",
      "Tiefbauamt des Kantons Schwyz",
      "Kantonspolizei Schwyz",
      "Eidg. Starkstrominspektorat",
      "Amt für öffentlichen Verkehr",
      "Amt für Raumentwicklung",
      "Verkehrsamt Schwyz",
      "Bezirk Einsiedeln",
      "Bezirk Gersau",
      "Bezirk Küssnacht",
      "Bezirk Höfe",
      "Bezirk March",
      "Bezirk Schwyz",
    ];

    ENV.APP.gisHost =
      "map.geo.sz.ch/mapserv_proxy?ogcserver=source for image/png";
  }

  return ENV;
};
