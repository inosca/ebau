"use strict";

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
  const appConfig = {
    kt_bern: {
      name: "be",
      realm: "ebau",
      locales: ["de", "fr"],
      supportGroups: [10000],
      useConfidential: false,
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
      features: {
        publication: {
          form: true,
          municipalityFilter: true,
        },
      },
    },
    kt_uri: {
      name: "ur",
      realm: "urec",
      locales: ["de"],
      supportGroups: [1070],
      useConfidential: true,
      completePreliminaryClarificationSlugs: [],
      selectableGroups: {
        roles: [
          1131, // Support
        ],
      },
      documents: {
        excludeFromDocuments: [],
      },
      instanceStates: instanceStatesUr,
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
      features: {
        publication: {
          form: false,
          municipalityFilter: false,
        },
      },
    },
  }[app];

  const oidcHost =
    process.env.KEYCLOAK_HOST || "http://camac-ng-keycloak.local";

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
    moment: {
      includeLocales: appConfig.locales,
    },

    languages: appConfig.locales,
    fallbackLanguage: "de",

    APPLICATION: appConfig,

    ebau: {
      internalURL: "http://camac-ng.local",
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
      internalForms: [
        "migriertes-dossier",
        "baupolizeiliches-verfahren",
        "zutrittsermaechtigung",
        "klaerung-baubewilligungspflicht",
      ],
    },
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

  return ENV;
};
