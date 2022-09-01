"use strict";

module.exports = function (environment) {
  const ENV = {
    modulePrefix: "camac-ng",
    environment,
    appEnv: process.env.APP_ENV || "development",
    rootURL: "/",
    locationType: "hash",
    podModulePrefix: "camac-ng/ui",
    historySupportMiddleware: true,
    maxDossierImportSize: 1000000000, // 1GB
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
    "ember-ebau-core": {
      gisUrl: "/lisag/ows",
      attachmentSections: { applicant: "12000000" },
    },
    APP: {
      rootElement: "#ember-camac-ng",
    },

    APPLICATIONS: {
      kt_bern: {
        name: "be",
        prodUrl: "ebau.apps.be.ch",
        gwr: {
          cantonAbbreviation: "BE",
          importModels: ["project"],
        },
        allowApplicantManualWorkItem: false,
        journalDefaultVisibility: false,
        journalEntryDuration: false,
        instanceStates: {
          archived: 20009,
        },
        interchangeableForms: [
          ["baugesuch", "baugesuch-generell", "baugesuch-mit-uvp"],
          ["baugesuch-v2", "baugesuch-generell-v2", "baugesuch-mit-uvp-v2"],
        ],
      },
      kt_schwyz: {
        name: "sz",
        prodUrl: "behoerden.ebau-sz.ch",
        gwr: {
          cantonAbbreviation: "SZ",
          importModels: ["project", "building", "dwelling"],
        },
        allowApplicantManualWorkItem: true,
        journalDefaultVisibility: false,
        journalEntryDuration: true,
        newCase: {
          calumaWorkflow: "internal-document",
          camacForm: 11,
        },
        externalServiceGroupIds: [],
      },
      kt_uri: {
        name: "ur",
        prodUrl: "urec.ur.ch",
        gwr: {
          cantonAbbreviation: "UR",
          importModels: ["project", "building", "dwelling"],
        },
        allowApplicantManualWorkItem: false,
        journalDefaultVisibility: true,
        journalEntryDuration: false,
        allowedInstanceLinkingGroups: [
          142, // KOOR BG
          21, // KOOR NP
        ],
        submittedStates: [
          21, // comm
          22, // ext
          23, // circ
          24, // redac
          25, // done
          26, // arch
          29, // nfd
          30, // subm
          31, // rejected
          32, // ext_gem
          33, // old
          34, // control
        ],
      },
    },

    // this will be overwritten by one of the canton specific configurations
    // above
    APPLICATION: {},
  };

  if (environment === "development") {
    ENV["ember-ebau-core"].gisUrl = "http://ebau.local/lisag/ows";
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

  ENV.APPLICATION = ENV.APPLICATIONS[process.env.APPLICATION || "kt_bern"];
  ENV.routerScroll = { targetElement: ENV.APP.rootElement };

  return ENV;
};
