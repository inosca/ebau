export default {
  name: "be",
  languages: ["de", "fr"],
  fallbackLanguage: "de",
  prodUrl: "www.ebau.apps.be.ch",
  gwr: {
    cantonAbbreviation: "BE",
    importModels: ["project"],
  },
  allowApplicantManualWorkItem: false,
  journalDefaultVisibility: false,
  journalEntryDuration: false,
  instanceStates: {
    new: 1,
    archived: 20009,
    coordination: 20005,
    circulationInit: 20003,
    finished: 120000,
    sb1: 20011,
  },
  interchangeableForms: [
    ["baugesuch", "baugesuch-generell", "baugesuch-mit-uvp"],
    ["baugesuch-v2", "baugesuch-generell-v2", "baugesuch-mit-uvp-v2"],
  ],
  useLocation: false,
  answerSlugs: {
    objectStreet: "strasse-flurname",
    objectNumber: "nr",
    objectZIP: "plz-grundstueck-v3",
    objectLocation: "ort-grundstueck",
    objectMigrated: "standort-migriert",
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
  decisionSlug: "decision-decision-assessment",
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
  intentSlugs: ["beschreibung-bauvorhaben"],
};
