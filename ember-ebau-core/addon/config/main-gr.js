export default {
  name: "gr",
  languages: ["de", "it"],
  fallbackLanguage: "de",
  prodUrl: "ebau.admin.gr.ch",
  allowApplicantManualWorkItem: false,
  serviceGroups: {
    authorityBaB: 3,
  },
  instanceStates: {
    new: 1,
    subm: 120004,
    circulation: 120005,
    correction: 120008,
  },
  answerSlugs: {
    objectStreet: "strasse-flurname",
    objectNumber: "nr",
    objectLocation: "ort-grundstueck",
    description: "beschreibung-bauvorhaben",
    municipality: "gemeinde",
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
        3, // municipality
      ],
      serviceGroups: [
        1, // municipality
      ],
    },
  },
  intentSlugs: ["beschreibung-bauvorhaben"],
};
