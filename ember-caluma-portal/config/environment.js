"use strict";

const locales = require("./locales");

module.exports = function (environment) {
  if (environment !== "production") {
    /* eslint-disable no-console */
    console.log("Build environment:");
    require("./dotenv")(environment).clientAllowedKeys.forEach((key) => {
      console.log(`\t${key}: ${process.env[key]}`);
    });
    /* eslint-enable no-console */
  }

  const app = process.env.APPLICATION || "kt_bern";
  const instanceStatesBe = {
    new: 1,
    rejected: 10000,
    subm: 20000,
    circulationInit: 20003,
    circulation: 20004,
    coordination: 20005,
    archived: 20009,
    evaluated: 20010,
    inCorrection: 20007,
    corrected: 20008,
    inProgress: 120001,
    inProgressInternal: 120002,
    finished: 120000,
    finishedInternal: 120003,
    sb1: 20011,
    sb2: 20013,
    conclusion: 20014,
  };
  const instanceStatesUr = {
    new: 28,
    finished: 25, // done
    archived: 26, // arch
    rejected: 31,
    old: 33,
  };
  const instanceStatesDemo = {
    new: 1,
    subm: 120004,
    circ: 120005,
    finished: 120006,
  };
  const instanceStatesGr = {
    new: 1,
    subm: 120004,
    circ: 120005,
    decision: 120007,
    inCorrection: 120008,
    circulationInit: 120009,
    constructionAcceptance: 120010,
    finished: 120006,
    rejected: 120011,
  };
  const instanceStatesSo = {
    new: 1,
    subm: 2,
    "material-exam": 3,
    "init-distribution": 4,
    distribution: 5,
    correction: 6,
    decision: 7,
    "construction-monitoring": 8,
    finished: 9,
    reject: 10,
    rejected: 11,
    withdrawn: 12,
    withdrawal: 13,
    decided: 14,
  };
  const appConfig = {
    demo: {
      name: "demo",
      realm: "ebau",
      supportGroups: [10000],
      useConfidential: false,
      defaultInstanceStateCategory: "pending",
      instanceStateCategories: {
        pending: [
          instanceStatesDemo.new,
          instanceStatesDemo.subm,
          instanceStatesDemo.circ,
        ],
        done: [instanceStatesDemo.finished],
      },
      completePreliminaryClarificationSlugs: [],
      selectableGroups: {
        roles: [
          3, // municipality
          10000, // support
        ],
      },
      documents: {
        backend: "alexandria",
        excludeFromDocuments: [],
      },
      instanceStates: instanceStatesDemo,
      // Who can create which forms. Roles can be given by ID, or magic key ("internal" or "public")
      formCreationPermissions: [
        {
          roles: ["public", "internal"],
          forms: ["baugesuch"],
        },
      ],
    },
    kt_bern: {
      name: "be",
      realm: "ebau",
      internalFrontend: "camac",
      supportGroups: [10000],
      defaultInstanceStateCategory: "pending",
      instanceStateCategories: {
        all: [
          instanceStatesBe.new,
          instanceStatesBe.subm,
          instanceStatesBe.circulationInit,
          instanceStatesBe.circulation,
          instanceStatesBe.coordination,
          instanceStatesBe.rejected,
          instanceStatesBe.inProgress,
          instanceStatesBe.inProgressInternal,
          instanceStatesBe.inCorrection,
          instanceStatesBe.corrected,
          instanceStatesBe.sb1,
          instanceStatesBe.sb2,
          instanceStatesBe.finished,
          instanceStatesBe.finishedInternal,
          instanceStatesBe.evaluated,
          instanceStatesBe.conclusion,
        ],
        pending: [
          instanceStatesBe.new,
          instanceStatesBe.subm,
          instanceStatesBe.circulationInit,
          instanceStatesBe.circulation,
          instanceStatesBe.coordination,
          instanceStatesBe.rejected,
          instanceStatesBe.inProgress,
          instanceStatesBe.inProgressInternal,
          instanceStatesBe.inCorrection,
          instanceStatesBe.corrected,
        ],
        sb: [instanceStatesBe.sb1, instanceStatesBe.sb2],
        done: [
          instanceStatesBe.finished,
          instanceStatesBe.finishedInternal,
          instanceStatesBe.evaluated,
          instanceStatesBe.conclusion,
        ],
      },
      completePreliminaryClarificationSlugs: [
        "vorabklaerung-vollstaendig",
        "vorabklaerung-vollstaendig-v2",
        "vorabklaerung-vollstaendig-v3",
        "vorabklaerung-vollstaendig-v4",
        "vorabklaerung-vollstaendig-v5",
      ],
      selectableGroups: {
        roles: [
          3, // Leitung Leitbehörde
          5, // Leitung Baukontrolle
          20004, // Sachbearbeiter Leitbehörde
          20005, // Sachbearbeiter Baukontrolle
          10000, // System-Betrieb
        ],
      },
      documents: {
        backend: "camac",
        feedbackSections: [3, 14], // Alle Beteiligten, Rechtsbegehren
        excludeFromDocuments: ["dokumente-platzhalter"],
      },
      instanceStates: instanceStatesBe,
      // Who can create which forms. Roles can be given by ID, or magic key ("internal" or "public")
      formCreationPermissions: [
        {
          roles: ["public", "internal"],
          forms: [
            "vorabklaerung-einfach",
            "vorabklaerung-vollstaendig",
            "baugesuch",
            "baugesuch-mit-uvp",
            "baugesuch-generell",
            "hecken-feldgehoelze-baeume",
            "solaranlagen-meldung",
            "heat-generator",
            "reklamegesuch",
          ],
        },
        {
          roles: ["internal"],
          forms: [
            "migriertes-dossier",
            "baupolizeiliches-verfahren",
            "zutrittsermaechtigung",
            "klaerung-baubewilligungspflicht",
          ],
        },
      ],
      staticSupportIds: { "heat-generator": 20046 },
    },
    kt_uri: {
      name: "ur",
      realm: "urec",
      internalFrontend: "camac",
      supportGroups: [1070],
      useConfidential: true,
      completePreliminaryClarificationSlugs: [],
      selectableGroups: {
        roles: [
          6, // Sekretariat der Gemeindebaubehörde
          3, // KOOR BG
          1061, // KOOR NP
          1101, // KOOR BD
          1106, // KOOR AfU
          1107, // KOOR ALA
          1127, // KOOR AfE
          1128, // KOOR AFJ
          1129, // KOOR SD
          1133, // KOOR AfG
          1130, // Bundesstelle
          1131, // Support
        ],
      },
      documents: {
        backend: "camac",
        excludeFromDocuments: [],
      },
      instanceStates: instanceStatesUr,
      defaultInstanceStateCategory: "notSubmitted",
      instanceStateCategories: {
        notSubmitted: [
          1, // new_comm
          28, // new
        ],
        submitted: [
          21, // comm
          22, // ext
          23, // circ
          24, // redac
          29, // nfd
          30, // subm
          31, // rejected
          32, // ext_gem
          25, // done
        ],
        done: [
          34, // control
          26, // arch
          27, // del
          33, // old
        ],
      },
      // Who can create which forms. Roles can be given by ID, or magic key ("internal" or "public")
      formCreationPermissions: [
        {
          roles: ["public"],
          forms: [
            "preliminary-clarification",
            "building-permit",
            "technische-bewilligung",
            "cantonal-territory-usage",
            "commercial-permit",
            "solar-declaration",
            "proposal-declaration",
            "bohrbewilligung-waermeentnahme",
            "konzession-waermeentnahme",
          ],
        },
        {
          // Sekretariat der Gemeindebaubehörde
          roles: [6],
          forms: [
            "solar-declaration",
            "preliminary-clarification",
            "oereb-verfahren-gemeinde",
            "commercial-permit",
            "building-permit",
            "proposal-declaration",
            "archivdossier",
            "pgv-gemeindestrasse",
            "technische-bewilligung",
          ],
        },
        {
          // KOOR BG
          roles: [3],
          forms: [
            "mitbericht-kanton",
            "mitbericht-bund",
            "bgbb",
            "archivdossier",
            "bauverwaltung",
          ],
        },
        {
          // KOOR NP
          roles: [1061],
          forms: ["mitbericht-kanton", "mitbericht-bund", "oereb"],
        },
        {
          // KOOR BD
          roles: [1101],
          forms: [
            "mitbericht-kanton",
            "mitbericht-bund",
            "cantonal-territory-usage",
            "commercial-permit",
            "oereb",
          ],
        },
        {
          // KOOR AfU
          roles: [1106],
          forms: ["mitbericht-kanton", "oereb"],
        },
        {
          // KOOR ALA
          roles: [1107],
          forms: ["mitbericht-kanton", "bgbb"],
        },
        {
          // KOOR AfE
          roles: [1127],
          forms: [
            "mitbericht-kanton",
            "bohrbewilligung-waermeentnahme",
            "konzession-waermeentnahme",
          ],
        },
        {
          // KOOR AfJ
          roles: [1128],
          forms: ["mitbericht-kanton", "oereb", "archivdossier"],
        },
        {
          // KOOR SD
          roles: [1129],
          forms: ["mitbericht-kanton", "cantonal-territory-usage"],
        },
        {
          // KOOR AfG
          roles: [1133],
          forms: ["mitbericht-kanton", "bgbb"],
        },
        {
          // Bundesstelle
          roles: [1130],
          forms: ["mitbericht-bund"],
        },
      ],
    },
    kt_gr: {
      name: "gr",
      realm: "ebau",
      internalFrontend: "ebau",
      supportGroups: [10000],
      defaultInstanceStateCategory: "pending",
      instanceStateCategories: {
        pending: [
          instanceStatesGr.new,
          instanceStatesGr.subm,
          instanceStatesGr.circulationInit,
          instanceStatesGr.circ,
          instanceStatesGr.inCorrection,
          instanceStatesGr.decision,
        ],
        decided: [instanceStatesGr.constructionAcceptance],
        done: [instanceStatesGr.finished, instanceStatesGr.rejected],
      },
      completePreliminaryClarificationSlugs: [],
      selectableGroups: {
        roles: [
          3, // municipality
          10000, // support
        ],
      },
      documents: {
        backend: "alexandria",
        excludeFromDocuments: [],
        feedbackSections: ["alle-beteiligten", "bauabnahme"],
      },
      instanceStates: instanceStatesGr,
      // Who can create which forms. Roles can be given by ID, or magic key ("internal" or "public")
      formCreationPermissions: [
        {
          roles: ["public", "internal"],
          forms: [
            "baugesuch",
            "vorlaeufige-beurteilung",
            "bauanzeige",
            "solaranlage",
          ],
        },
      ],
    },
    kt_so: {
      name: "so",
      realm: "ebau",
      internalFrontend: "ebau",
      supportGroups: [3],
      defaultInstanceStateCategory: "all",
      instanceStateCategories: {
        all: Object.values(instanceStatesSo),
        pending: [
          instanceStatesSo.new,
          instanceStatesSo.subm,
          instanceStatesSo["material-exam"],
          instanceStatesSo["init-distribution"],
          instanceStatesSo.distribution,
          instanceStatesSo.correction,
          instanceStatesSo.decision,
          instanceStatesSo.reject,
        ],
        decided: [
          instanceStatesSo.decided,
          instanceStatesSo["construction-monitoring"],
        ],
        done: [
          instanceStatesSo.finished,
          instanceStatesSo.rejected,
          instanceStatesSo.withdrawal,
          instanceStatesSo.withdrawn,
        ],
      },
      completePreliminaryClarificationSlugs: [],
      selectableGroups: {
        roles: [
          3, // Support
          5, // Municipality lead
        ],
      },
      documents: {
        backend: "alexandria",
        excludeFromDocuments: [],
      },
      instanceStates: instanceStatesSo,
      // Who can create which forms. Roles can be given by ID, or magic key ("internal" or "public")
      formCreationPermissions: [
        {
          roles: ["public", "internal"],
          forms: [
            "baugesuch",
            "erdwaermesonden",
            "voranfrage",
            "meldung",
            "meldung-pv",
          ],
        },
      ],
    },
  }[app];

  const oidcHost = process.env.KEYCLOAK_HOST || "http://ebau-keycloak.local";
  const oidcRealm = process.env.KEYCLOAK_REALM || appConfig.realm;
  const internalURL =
    process.env.INTERNAL_URL ||
    (appConfig.internalFrontend === "camac"
      ? "http://ebau.local"
      : "http://ember-ebau.local");
  const beGisUrl = process.env.BE_GIS_URL || "https://www.map.apps.be.ch";
  const urGisUrl = process.env.UR_GIS_URL || "https://geo.ur.ch/wms";

  const ENV = {
    modulePrefix: "caluma-portal",
    environment,
    rootURL: "/",
    locationType: "history",
    profileURL: `${oidcHost}/auth/realms/${oidcRealm}/account?referrer=portal#/personal-info`,
    historySupportMiddleware: true,
    "ember-simple-auth-oidc": {
      host: `${oidcHost}/auth/realms/${oidcRealm}/protocol/openid-connect`,
      clientId: "portal",
      authEndpoint: "/auth",
      tokenEndpoint: "/token",
      endSessionEndpoint: "/logout",
      userinfoEndpoint: "/userinfo",
      afterLogoutUri: "/login",
      loginHintName: "kc_idp_hint",
      enablePkce: true,
    },
    "ember-ebau-core": {
      attachmentSections: { applicant: "12000000" },
      urGisUrl,
    },
    "ember-caluma": {
      FLATPICKR_DATE_FORMAT: {
        de: "d.m.Y",
        fr: "d.m.Y",
        it: "d.m.Y",
        en: "m/d/Y",
      },
      FLATPICKR_DATE_FORMAT_DEFAULT: "d.m.Y",
    },
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
      // Here you can pass flags/options to your application instance
      // when it is created
    },

    languages: locales,
    fallbackLanguage: "de",

    APPLICATION: appConfig,

    ebau: {
      beGisUrl,
      internalURL,
      supportGroups: appConfig.supportGroups,
      selectableGroups: appConfig.selectableGroups,
    },
  };

  if (environment === "development") {
    ENV.ebau.beGisUrl = "https://www.map2-test.apps.be.ch";
    ENV["ember-ebau-core"].urGisUrl = "/lisag/wms";
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
