const config = {
  name: "so",
  languages: ["de"],
  fallbackLanguage: "de",
  allowApplicantManualWorkItem: false,
  instanceStates: {
    new: 1,
    subm: 2,
    "formal-exam": 3,
    "init-distribution": 4,
    distribution: 5,
    correction: 6,
  },
  answerSlugs: {
    objectStreet: "strasse-flurname",
    objectNumber: "strasse-nummer",
    objectLocation: "ort",
    description: "umschreibung-bauprojekt",
    municipality: "gemeinde",
    specialId: "dossier-number",
    parcel: "parzellen",
    parcelNumber: "parzellennummer",
    firstNameApplicant: "vorname",
    lastNameApplicant: "nachname",
    juristicNameApplicant: "juristische-person-name",
    isJuristicApplicant: "juristische-person",
    isJuristicApplicantYes: "juristische-person-ja",
    personalDataApplicant: "bauherrin",
  },
  personalSuggestions: {
    tableQuestions: ["bauherrin", "grundeigentuemerin", "projektverfasserin"],
    firstNameRegexp: "^vorname$",
    lastNameRegexp: "^nachname$",
    juristicNameRegexp: "^juristische-person-name$",
    emailRegexp: "^e-mail$",
  },
  paperInstances: {
    allowedGroups: {
      roles: [],
      serviceGroups: [],
    },
  },
  correction: {
    instanceState: "correction",
    allowedInstanceStates: [
      "subm",
      "formal-exam",
      "init-distribution",
      "distribution",
    ],
  },
};

config.intentSlugs = [config.answerSlugs.description];

export default config;
