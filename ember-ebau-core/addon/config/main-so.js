export default {
  name: "so",
  languages: ["de"],
  fallbackLanguage: "de",
  allowApplicantManualWorkItem: false,
  instanceStates: {
    new: 1,
  },
  answerSlugs: {
    objectStreet: "strasse-flurname",
    objectNumber: "strasse-nummer",
    objectLocation: "ort",
    description: "umschreibung-bauprojekt",
    municipality: "gemeinde",
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
  intentSlugs: [],
  paperInstances: {
    allowedGroups: {
      roles: [],
      serviceGroups: [],
    },
  },
};
