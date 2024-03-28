const config = {
  name: "so",
  languages: ["de"],
  fallbackLanguage: "de",
  allowApplicantManualWorkItem: false,
  documentBackend: "alexandria",
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
      rejected: "entscheid-entscheid-beschwerde-zurueckgewiesen",
    },
    colorMapping: {
      "entscheid-entscheid-zustimmung": "uk-alert-success",
      "entscheid-entscheid-ablehnung": "uk-alert-danger",
      "entscheid-entscheid-teilzustimmung": "uk-alert-warning",
      "entscheid-entscheid-rueckzug": "uk-alert-warning",
    },
  },
  appeal: {
    instanceStates: {
      decision: "decision",
      afterPositive: "construction-monitoring",
      afterNegative: "finished",
    },
    answerSlugs: {
      "entscheid-entscheid-beschwerde-bestaetigt": "confirmed",
      "entscheid-entscheid-beschwerde-geaendert": "changed",
      "entscheid-entscheid-beschwerde-aufgehoben": "annulled",
      "entscheid-entscheid-beschwerde-zurueckgewiesen": "rejected",
    },
    info: {
      confirmed: {
        color: "success",
        status: (prevPositive) =>
          prevPositive ? "construction-monitoring" : "finished",
      },
      changed: {
        color: "warning",
        status: () => "construction-monitoring",
      },
      annulled: {
        color: "danger",
        status: () => "finished",
      },
      rejected: {
        color: "danger",
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
};

config.intentSlugs = [config.answerSlugs.description];

export default config;
