const config = {
  name: "so",
  languages: ["de"],
  fallbackLanguage: "de",
  allowApplicantManualWorkItem: false,
  instanceStates: {
    new: 1,
    subm: 2,
    "material-exam": 3,
    "init-distribution": 4,
    distribution: 5,
    correction: 6,
    reject: 10,
    rejected: 11,
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
      "material-exam",
      "init-distribution",
      "distribution",
    ],
  },
  publication: {
    public: {
      task: "fill-publication",
      startQuestion: "publikation-start",
      endQuestion: "publikation-ende",
    },
  },
  decision: {
    task: "decision",
    answerSlugs: {
      decision: "entscheid-entscheid",
      remarks: "entscheid-bemerkungen",
    },
    colorMapping: {
      "entscheid-entscheid-zustimmung": "uk-alert-success",
      "entscheid-entscheid-ablehnung": "uk-alert-danger",
      "entscheid-entscheid-teilzustimmung": "uk-alert-warning",
      "entscheid-entscheid-rueckzug": "uk-alert-warning",
    },
  },
  alexandria: {
    enabledMarks: ["decision", "publication", "void"],
  },
  legalSubmission: {
    task: "objections",
    tableForm: "einsprache",
    tableQuestion: "einsprachen",
    orderQuestion: "einsprache-datum",
    columns: {
      date: "einsprache-datum",
      "legal-claimants": "einsprache-einsprechende",
      withdrawn: "einsprache-zurueckgezogen",
    },
  },
  rejection: {
    instanceState: "rejected",
    allowedInstanceStates: ["reject"],
  },
};

config.intentSlugs = [config.answerSlugs.description];

export default config;
