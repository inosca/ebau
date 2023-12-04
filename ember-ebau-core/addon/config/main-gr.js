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
    "init-distribution": 120009,
    rejected: 120011,
  },
  answerSlugs: {
    objectStreet: "street-and-housenumber",
    objectLocation: "ort-grundstueck",
    description: "beschreibung-bauvorhaben",
    municipality: "gemeinde",
    specialId: "dossier-number",
    parcel: "parzelle",
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
        2, // municipality
      ],
    },
  },
  intentSlugs: ["beschreibung-bauvorhaben"],
  correction: {
    instanceState: "correction",
    allowedInstanceStates: ["subm", "init-distribution", "circulation"],
  },
  publication: {
    public: {
      task: "fill-publication",
    },
  },
  decision: {
    task: "decision",
    answerSlugs: {
      decision: "decision-decision",
      remarks: "decision-remarks",
    },
    colorMapping: {
      "decision-decision-approved": "uk-alert-success",
      "decision-decision-rejected": "uk-alert-danger",
      "decision-decision-written-off": "uk-alert-warning",
      "decision-decision-positive": "uk-alert-success",
      "decision-decision-negative": "uk-alert-danger",
      "decision-decision-positive-with-reservation": "uk-alert-warning",
      "decision-decision-retreat": "uk-alert-warning",
    },
  },
  alexandria: {
    enabledMarks: ["decision", "publication", "void"],
  },
  rejection: {
    instanceState: "rejected",
    allowedInstanceStates: ["subm", "init-distribution"],
  },
};
