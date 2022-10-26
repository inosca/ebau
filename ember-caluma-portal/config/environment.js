"use strict";

const locales = require("./locales");

module.exports = function (environment) {
  // eslint-disable-next-line no-console
  console.log(
    `build env: APPLICATION: ${process.env.APPLICATION}, KEYCLOAK_HOST: ${process.env.KEYCLOAK_HOST}`
  );
  const app = process.env.APPLICATION || "kt_bern";
  const instanceStatesBe = {
    new: 1,
    rejected: 10000,
    archived: 20009,
    inCorrection: 20007,
    finished: 120000,
    sb1: 20011,
    sb2: 20013,
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
    finished: 120006,
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
          1, // new
        ],
        done: [
          120004, // finished
        ],
      },
      completePreliminaryClarificationSlugs: [
        "vorabklaerung-vollstaendig",
        "vorabklaerung-vollstaendig-v2",
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
        feedbackSection: 3,
        excludeFromDocuments: ["dokumente-platzhalter"],
      },
      instanceStates: instanceStatesDemo,
      modification: {
        allowForms: ["baugesuch"],
        disallowStates: [instanceStatesDemo.new, instanceStatesDemo.finished],
      },
      answerSlugs: {},
      personalSuggestions: {
        tableQuestions: [
          "personalien-gesuchstellerin",
          "personalien-vertreterin-mit-vollmacht",
          "personalien-grundeigentumerin",
          "personalien-projektverfasserin",
          "personalien-gebaudeeigentumerin",
          "personalien-sb",
        ],
        firstNameRegexp: "^vorname-.*$",
        lastNameRegexp: "^name-.*$",
        juristicNameRegexp: "^name-juristische-person.*$",
        emailRegexp: "^e-mail-.*$",
      },
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
      supportGroups: [10000],
      useConfidential: false,
      defaultInstanceStateCategory: "pending",
      instanceStateCategories: {
        pending: [
          1, // new
          20003, // circulation_init
          20004, // circulation
          20005, // coordination
        ],
        done: [
          120000, // finished
        ],
      },
      completePreliminaryClarificationSlugs: [],
      selectableGroups: {
        roles: [
          3, // Leitung Leitbehörde
          10000, // System-Betrieb
        ],
      },
      documents: {
        excludeFromDocuments: [],
      },
      instanceStates: instanceStatesBe,
      modification: {
        allowForms: [
          "baugesuch",
          "baugesuch-v2",
          "baugesuch-generell",
          "baugesuch-generell-v2",
          "baugesuch-mit-uvp",
          "baugesuch-mit-uvp-v2",
        ],
        disallowStates: [
          instanceStatesBe.new,
          instanceStatesBe.archived,
          instanceStatesBe.finished,
        ],
      },
      answerSlugs: {
        objectStreet: "strasse-flurname",
        objectNumber: "nr",
        objectLocation: "ort-grundstueck",
        description: "beschreibung-bauvorhaben",
        municipality: "gemeinde",
        specialId: "ebau-number",
        parcelNumber: "parzellennummer",
        firstNameApplicant: "vorname-gesuchstellerin",
        lastNameApplicant: "name-gesuchstellerin",
        juristicNameApplicant: "name-juristische-person-gesuchstellerin",
        isJuristicApplicant: "juristische-person-gesuchstellerin",
        isJuristicApplicantYes: "juristische-person-gesuchstellerin-ja",
        personalDataApplicant: "personalien-gesuchstellerin",
      },
      personalSuggestions: {
        tableQuestions: [
          "personalien-gesuchstellerin",
          "personalien-vertreterin-mit-vollmacht",
          "personalien-grundeigentumerin",
          "personalien-projektverfasserin",
          "personalien-gebaudeeigentumerin",
          "personalien-sb",
        ],
        firstNameRegexp: "^vorname-.*$",
        lastNameRegexp: "^name-.*$",
        juristicNameRegexp: "^name-juristische-person.*$",
        emailRegexp: "^e-mail-.*$",
      },
      paperInstances: {
        allowedGroups: {
          roles: [
            3, // Leitung Leitbehörde
            20004, // Sachbearbeiter Leitbehörde
          ],
          serviceGroups: [
            2, // Gemeinde
            20000, // Regierungsstatthalteramt
          ],
        },
      },
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
    },
    kt_uri: {
      name: "ur",
      realm: "urec",
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
          1130, // Bundesstelle
          1131, // Support
        ],
      },
      documents: {
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
          34, // control
        ],
        done: [
          25, // done
          26, // arch
          27, // del
          33, // old
        ],
      },
      modification: {
        allowForms: ["building-permit"],
        disallowStates: [
          instanceStatesUr.new,
          instanceStatesUr.archived,
          instanceStatesUr.finished,
          instanceStatesUr.old,
        ],
      },
      answerSlugs: {
        objectStreet: "parcel-street",
        objectNumber: "street-number",
        objectLocation: "parcel-city",
        applicantZip: "zip",
        description: "proposal-description",
        municipality: "municipality",
        specialId: "dossier-number",
        parcelNumber: "parcel-number",
        oerebProcedure: "typ-des-verfahrens",
        oerebTopics: "oereb-thema",
        oerebPartialState: "teilstatus",
        procedureCanton: "mbv-type",
        procedureConfederation: "mbv-bund-type",
      },
      personalSuggestions: {
        tableQuestions: [
          "applicant",
          "landowner",
          "project-author",
          "invoice-recipient",
        ],
        firstNameRegexp: "^first-name$",
        lastNameRegexp: "^last-name$",
        juristicNameRegexp: "^juristic-person-name$",
        emailRegexp: "^e-mail$",
      },
      paperInstances: {
        allowedGroups: {
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
            1130, // Bundesstelle
            1131, // Support
          ],
          serviceGroups: [
            1, // Koordinationsstellen
            68, // Sekretariate Gemeindebaubehörden
            70, // Bundesstellen
          ],
        },
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
          ],
        },
        {
          // Sekretariat der Gemeindebaubehörde
          roles: [6],
          forms: [
            "solar-declaration",
            "preliminary-clarification",
            "oereb",
            "commercial-permit",
            "building-permit",
            "proposal-declaration",
            "archivdossier",
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
            "bohrbewilligung-waermeentnahme",
            "konzession-waermeentnahme",
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
          forms: ["mitbericht-kanton"],
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
          // Bundesstelle
          roles: [1130],
          forms: ["mitbericht-bund"],
        },
      ],
    },
  }[app];

  const oidcHost = process.env.KEYCLOAK_HOST || "http://ebau-keycloak.local";
  const internalURL = process.env.INTERNAL_URL || "http://ebau.local";
  const beGisUrl = process.env.BE_GIS_URL || "https://www.map.apps.be.ch";

  const ENV = {
    modulePrefix: "caluma-portal",
    environment,
    rootURL: "/",
    locationType: "auto",
    historySupportMiddleware: true,
    "ember-simple-auth-oidc": {
      host: `${oidcHost}/auth/realms/${appConfig.realm}/protocol/openid-connect`,
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
      gisUrl: "/lisag/ows",
      attachmentSections: { applicant: "12000000" },
    },
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
      // Here you can pass flags/options to your application instance
      // when it is created
    },

    languages: locales,
    fallbackLanguage: "de",

    APPLICATION: appConfig,

    ebau: {
      beGisUrl,
      internalURL,
      attachments: {
        allowedMimetypes: ["image/png", "image/jpeg", "application/pdf"],
        buckets: [
          "dokument-grundstucksangaben",
          "dokument-gutachten-nachweise-begrundungen",
          "dokument-projektplane-projektbeschrieb",
          "dokument-weitere-gesuchsunterlagen",
        ],
      },
      supportGroups: appConfig.supportGroups,
      selectableGroups: appConfig.selectableGroups,
    },
  };

  if (environment === "development") {
    ENV["ember-ebau-core"].gisUrl = "http://ebau.local/lisag/ows";
    ENV.ebau.beGisUrl = "https://www.map2-test.apps.be.ch";
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
