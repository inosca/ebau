export default {
  name: "be",
  languages: ["de", "fr"],
  fallbackLanguage: "de",
  prodUrl: "www.ebau.apps.be.ch",
  showInstanceIdAfterSubmission: true,
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
    sb2: 20013,
    conclusion: 20014,
    evaluated: 20010,
    finishedInternal: 120003,
    rejected: 10000,
    circulation: 20004,
  },
  interchangeableForms: [
    ["baugesuch", "baugesuch-generell", "baugesuch-mit-uvp"],
    ["baugesuch-v2", "baugesuch-generell-v2", "baugesuch-mit-uvp-v2"],
    ["baugesuch-v3", "baugesuch-generell-v3", "baugesuch-mit-uvp-v3"],
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
  publication: {
    neighbors: {
      task: "information-of-neighbors",
      startQuestion: "information-of-neighbors-start-date",
      endQuestion: "information-of-neighbors-end-date",
    },
    public: {
      task: "fill-publication",
      startQuestion: "publikation-startdatum",
      endQuestion: "publikation-ablaufdatum",
    },
  },
  decision: {
    task: "decision",
    answerSlugs: {
      decision: "decision-decision-assessment",
      remarks: "decision-remarks",
    },
    colorMapping: {
      "decision-decision-assessment-positive": "uk-alert-success",
      "decision-decision-assessment-accepted": "uk-alert-success",
      "decision-decision-assessment-negative": "uk-alert-danger",
      "decision-decision-assessment-denied": "uk-alert-danger",
      "decision-decision-assessment-positive-with-reservation":
        "uk-alert-warning",
      "decision-decision-assessment-retreat": "uk-alert-warning",
    },
  },
  billing: {
    readOnlyInstanceStates: [
      "sb1",
      "sb2",
      "conclusion",
      "evaluated",
      "finished",
      "finishedInternal",
    ],
  },
  rejection: {
    instanceState: "rejected",
    allowedInstanceStates: ["circulationInit", "circulation"],
  },
};
