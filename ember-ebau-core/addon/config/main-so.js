const config = {
  name: "so",
  languages: ["de"],
  fallbackLanguage: "de",
  allowApplicantManualWorkItem: false,
  documentBackend: "alexandria",
  showIdInInternalArea: false,
  instanceStates: {
    new: 1,
    subm: 2,
    "material-exam": 3,
    "init-distribution": 4,
    distribution: 5,
    correction: 6,
    decision: 7,
    "construction-monitoring": 8,
    finished: 9,
    reject: 10,
    rejected: 11,
    withdrawn: 12,
    withdrawal: 13,
    decided: 14,
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
      roles: [5],
      serviceGroups: [1],
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
      "entscheid-entscheid-positiv": "uk-alert-success",
      "entscheid-entscheid-negativ": "uk-alert-danger",
    },
  },
  appeal: {
    instanceStates: {
      decision: "decision",
      afterPositive: "decided",
      afterNegative: "decided",
    },
    answerSlugs: {
      "entscheid-entscheid-beschwerde-bestaetigt": "confirmed",
      "entscheid-entscheid-beschwerde-geaendert": "changed",
      "entscheid-entscheid-beschwerde-zurueckgewiesen": "rejected",
      willGenerateCopy: [
        "entscheid-entscheid-beschwerde-geaendert",
        "entscheid-entscheid-beschwerde-zurueckgewiesen",
      ],
    },
    info: {
      confirmed: {
        color: "default",
        status: () => "decided",
      },
      changed: {
        color: "default",
        status: () => "decision",
      },
      rejected: {
        color: "default",
        status: () => "subm",
      },
    },
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
  withdrawal: {
    allowedInstanceStates: [
      "subm",
      "material-exam",
      "init-distribution",
      "distribution",
      "decision",
    ],
  },
  alexandria: {
    marks: {
      decision: "decision",
      objection: "objection",
      void: "void",
    },
  },
  gwr: {
    cantonAbbreviation: "SO",
    importModels: ["project", "building", "dwelling"],
    modalContainer: "body",
  },
  communication: {
    rolesWithApplicantContact: ["activeOrInolvedLeadAuthority"],
  },
  dossierImport: {
    municipalityAdminRole: 4, // Administration Gemeinde
    municipalityServiceGroup: 1, // Gemeinde
  },
  constructionMonitoring: {
    instanceStates: ["construction-monitoring", "finished"],
  },
};

config.intentSlugs = [config.answerSlugs.description];
config.submittedStates = Object.entries(config.instanceStates)
  .filter(([name]) => name !== "new")
  .map(([, id]) => id);

export default config;
