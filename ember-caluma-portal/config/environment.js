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
      },
      instanceStates: instanceStatesBe,
      modification: {
        allowForms: ["baugesuch", "baugesuch-generell", "baugesuch-mit-uvp"],
        disallowStates: [
          instanceStatesBe.new,
          instanceStatesBe.rejected,
          instanceStatesBe.archived,
          instanceStatesBe.inCorrection,
          instanceStatesBe.finished,
          instanceStatesBe.sb1,
          instanceStatesBe.sb2,
        ],
      },
      answerSlugs: {
        objectStreet: "strasse-flurname",
        applicantStreet: "strasse-gesuchstellerin",
        objectNumber: "nr",
        applicantNumber: "nummer-gesuchstellerin",
        objectLocation: "ort-grundstueck",
        applicantLocation: "ort-gesuchstellerin",
        constructionDescription: "beschreibung-bauvorhaben",
        municipality: "gemeinde",
        specialId: "ebau-number",
      },
    },
    kt_uri: {
      name: "ur",
      realm: "urec",
      locales: ["de"],
      supportGroups: [1070],
      useConfidential: true,
      selectableGroups: {
        roles: [
          1131, // Support
        ],
      },
      documents: {},
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
        applicantStreet: "street",
        objectNumber: "street-number",
        applicantNumber: "street-number",
        objectLocation: "parcel-city",
        applicantLocation: "city",
        constructionDescription: "proposal-description",
        municipality: "municipality",
        specialId: "dossier-number",
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
