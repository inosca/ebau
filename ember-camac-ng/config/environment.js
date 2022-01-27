"use strict";

const locales = require("./locales");

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
    moment: {
      includeLocales: locales,
      allowEmpty: true,
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

    caseFilters: {
      instanceId: {
        type: "input",
      },
      dossierNumber: {
        type: "input",
      },
      applicantName: {
        type: "input",
      },
      street: {
        type: "input",
      },
      municipality: {
        type: "select",
        options: "municipalities",
        valueField: "id",
        labelField: "name",
      },
      parcelNumber: {
        type: "input",
      },
      instanceState: {
        type: "select",
        options: "instanceStates",
        valueField: "id",
        labelField: "uppercaseName",
      },
      service: {
        type: "select",
        options: "services",
        valueField: "id",
        labelField: "name",
      },
      pendingSanctionsControlInstance: {
        type: "select",
        options: "services",
        valueField: "id",
        labelField: "name",
      },
      buildingPermitType: {
        type: "select",
        options: "buildingPermitTypes",
      },
      createdAfter: {
        type: "date",
        maxDate: "createdBefore",
      },
      createdBefore: {
        type: "date",
        minDate: "createdAfter",
      },
      intent: {
        type: "input",
      },
      caseStatus: {
        type: "select",
        options: "caseStatusOptions",
        optionValues: ["RUNNING", "COMPLETED", "CANCELED", "SUSPENDED"],
        valueField: "status",
        labelField: "label",
      },
      caseDocumentFormName: {
        type: "input",
      },
    },

    APPLICATIONS: {
      kt_bern: {
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
        caseTableColumns: [
          "dossierNr",
          "caseDocumentFormName",
          "intent",
          "caseStatus",
        ],
        activeCaseFilters: [
          "dossierNumber",
          "intent",
          "caseStatus",
          "caseDocumentFormName",
        ],
        intentSlugs: ["internes-geschaeft-vorhaben"],
      },
      kt_uri: {
        prodUrl: "camac.ur.ch",
        gwr: {
          cantonAbbreviation: "UR",
          importModels: ["project", "building", "dwelling"],
        },
        allowApplicantManualWorkItem: false,
        journalDefaultVisibility: true,
        journalEntryDuration: false,
        activeCirculationStates: [
          1, // RUN
          41, // NFD
        ],
        allowedInstanceLinkingGroups: [
          142, // KOOR BG
          21, // KOOR NP
        ],
        caseTableColumns: {
          municipality: [
            "instanceId",
            "dossierNr",
            "form",
            "municipality",
            "user",
            "applicant",
            "intent",
            "street",
            "instanceState",
          ],
          coordination: [
            "instanceId",
            "dossierNr",
            "coordination",
            "form",
            "municipality",
            "user",
            "applicant",
            "intent",
            "street",
            "instanceState",
          ],
          service: [
            "deadlineColor",
            "instanceId",
            "dossierNr",
            "coordination",
            "form",
            "municipality",
            "applicant",
            "intent",
            "street",
            "processingDeadline",
          ],
          default: [
            "dossierNr",
            "municipality",
            "applicant",
            "intent",
            "street",
            "parcelNumbers",
          ],
        },
        activeCaseFilters: [
          "instanceId",
          "dossierNumber",
          "applicantName",
          "street",
          "municipality",
          "parcelNumber",
          "instanceState",
          "service",
          "pendingSanctionsControlInstance",
          "buildingPermitType",
          "createdAfter",
          "createdBefore",
          "intent",
        ],
        intentSlugs: [
          "proposal-description",
          "beschreibung-zu-mbv",
          "bezeichnung",
          "vorhaben-proposal-description",
          "veranstaltung-beschrieb",
        ],
      },
    },

    // this will be overwritten by one of the canton specific configurations
    // above
    APPLICATION: {},
  };

  if (environment === "development") {
    ENV["ember-ebau-core"].gisUrl = "http://camac-ng.local/lisag/ows";
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
