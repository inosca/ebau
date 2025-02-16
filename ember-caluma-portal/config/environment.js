"use strict";

const locales = require("./locales");

module.exports = function (environment) {
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
    withdrawn: 120012,
    withdrawal: 120013,
  };
  const instanceStatesAg = {
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
        excludeFromDocuments: [
          "dokumente-platzhalter",
          "grundstuecksentwaesserungsplan-dokument-begruendung-v5",
          "vollmacht-dokument-begruendung-v5",
          "vorabklaerung-dokument-begruendung-v5",
          "sicherungsmassnahme-dokument-begruendung-v5",
          "berechnungen-abstellplaetze-dokument-begruendung-v5",
          "ausnuetzung-dokument-begruendung-v5",
          "gruenflaeche-dokument-begruendung-v5",
          "ueberbauung-dokument-begruendung-v5",
          "geschossflaechen-dokument-begruendung-v5",
          "regierungsratsbeschluss-bauinventar-dokument-begruendung-v5",
          "vertrag-zum-bauinventar-dokument-begruendung-v5",
          "inanspruchnahme-boden-dokument-begruendung-v5",
          "anschluss-sammelkanaele-vorfluter-dokument-begruendung-v5",
          "zustimmung-der-anstoesser-dokument-begruendung-v5",
          "brandschutzkonzept-dokument-begruendung-v5",
          "brandschutzplan-dokument-begruendung-v5",
          "qualitaetssicherungskonzept-dokument-begruendung-v5",
          "weitere-angaben-regeneration-ews-dokument-begruendung-v5",
          "formular-andere-thermoaktive-elemente-dokument-begruendung-v5",
          "sondenmodell-mit-datenblatt-dokument-begruendung-v5",
          "erdwaermensondendimensionierung-dokument-begruendung-v5",
          "hydrogeologische-begleitung-dokument-begruendung-v5",
          "hydrogeo-gutachten-dokument-begruendung-v5",
          "sicherungsleistung-befreit-dokument-begruendung-v5",
          "schutzraum-dokument-begruendung-v5",
          "betriebskonzept-gastgewerbe-dokument-begruendung-v5",
          "beschrieb-der-lueftung-dokument-begruendung-v5",
          "grundriss-angabe-bodenflaeche-dokument-begruendung-v5",
          "plane-gastgewerbebetrieb-dokument-begruendung-v5",
          "plaene-fumoir-dokument-begruendung-v5",
          "situationsplan-dokument-begruendung-v5",
          "grundriss-dokument-begruendung-v5",
          "schnitt-dokument-begruendung-v5",
          "kurzbericht-risikoermittlung-dokument-begruendung-v5",
          "auszug-konsultationsbereichskarte-stoerfallverordnung-kt-bern-begruendung-v5",
          "entwaesserung-ueber-regenwasserkanal-dokument-begruendung-v5",
          "entwaesserung-oberflaechengewaesser-dokument-begruendung-v5",
          "entwaesserung-ueber-mischwasserkanal-dokument-begruendung-v5",
          "kanalisationskatasterplan-dokument-begruendung-v5",
          "versickerungsanlagen-dokument-begruendung-v5",
          "gewaesserschutz-landwirtschaft-dokument-begruendung-v5",
          "bestaetigung-hydrogeo-begleitung-dokument-begruendung-v5",
          "schnittplan-gewaesserschutz-dokument-begruendung-v5",
          "plaene-gewaesserschutz-dokument-begruendung-v5",
          "baugrunduntersuchung-dokument-begruendung-v5",
          "gesuch-ausnahmebewilligung-dokument-begruendung-v5",
          "energiedokumente-dokument-begruendung-v5",
          "gesuch-erleichterung-waermeschutz-dokument-begruendung-v5",
          "ausnahmegesuch-energie-dokument-begruendung-v5",
          "gesuch-zur-ausnahme-dokument-begruendung-v5",
          "nachweis-anforderungen-dokument-begruendung-v5",
          "rueckbau-checkliste-selbstdeklaration-dokument-begruendung-v5",
          "entsorgungskonzept-dokument-begruendung-v5",
          "bodenschutzkonzept-dokument-begruendung-v5",
          "meldeblatt-fuer-terrainveraenderungen-dokument-begruendung-v5",
          "verwertung-von-abgetragenem-boden-dokument-begruendung-v5",
          "plan-temporaere-definitive-flaeche-dokument-begruendung-v5",
          "rodungsgesuchsformular-bafu-dokument-begruendung-v5",
          "uebersichtsplan-dokument-begruendung-v5",
          "rodungs-und-ersatzaufforstungsplan-dokument-begruendung-v5",
          "gefahrengutachten-dokument-begruendung-v5",
          "fassadenplan-reklamestandort-dokument-begruendung-v5",
          "skizze-der-reklame-mit-farbangaben-dokument-begruendung-v5",
          "nachweis-raumakustik-dokument-begruendung-v5",
          "kataster-werkleitungsplaene-dokument-begruendung-v5",
          "situationsplan-grabflaeche-strassenterrainflaeche-dokument-begruendung-v5",
          "heat-generator-minergie-document-begruendung-v3",
          "heat-generator-geak-document-begruendung-v3",
          "heat-generator-standard-solution-document-begruendung-v3",
          "heat-generator-more-renewable-gas-document-begruendung-v3",
          "situationsplan-hecken-feldgehoelze-baeume-dokument-begruendung-v2",
          "baumfaellgutachten-dokument-begruendung-v2",
          "baumfaellbegruendung-dokument-begruendung-v2",
          "situationsplan-ersatzpflanzung-und-rodung-dokument-begruendung-v2",
          "entfernen-von-hecken-und-feldgehoelzen-dokument-begruendung-v2",
          "solaranlagen-tabelle-grundriss-ansichtsplan-dokument-begruendung-v2",
        ],
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
            "benuetzung-oeffentlichem-terrain-meldung",
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
      staticSupportIds: {
        "heat-generator": 20046,
        "heat-generator-v2": 20046,
        "heat-generator-v3": 20046,
      },
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
            "archivdossier",
            "pgv-gemeindestrasse",
            "oereb-verfahren-gemeinde",
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
        done: [
          instanceStatesGr.finished,
          instanceStatesGr.rejected,
          instanceStatesGr.withdrawal,
          instanceStatesGr.withdrawn,
        ],
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
            "reklamegesuch",
          ],
        },
      ],
    },
    kt_ag: {
      name: "ag",
      realm: "ebau",
      internalFrontend: "ebau",
      supportGroups: [10000],
      defaultInstanceStateCategory: "pending",
      instanceStateCategories: {
        pending: [
          instanceStatesAg.new,
          instanceStatesAg.subm,
          instanceStatesAg.circulationInit,
          instanceStatesAg.circ,
          instanceStatesAg.inCorrection,
          instanceStatesAg.decision,
        ],
        decided: [instanceStatesAg.constructionAcceptance],
        done: [instanceStatesAg.finished, instanceStatesAg.rejected],
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
      instanceStates: instanceStatesAg,
      // Who can create which forms. Roles can be given by ID, or magic key ("internal" or "public")
      formCreationPermissions: [
        {
          roles: ["public", "internal"],
          forms: [
            "baugesuch",
            "baugesuch-mit-uvp",
            "vorentscheid",
            "anfrage",
            "reklame",
            "plangenehmigungsverfahren-bund",
            "plangenehmigungsverfahren-gas",
            "vorabklaerung",
            "anfrage-intern",
            "baugesuch-migration",
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
      USE_MANDATORY_ASTERISK: process.env.APPLICATION === "kt_ag",
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
