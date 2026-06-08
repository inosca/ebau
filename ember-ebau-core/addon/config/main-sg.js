const config = {
  name: "sg",
  languages: ["de"],
  fallbackLanguage: "de",
  prodUrl: "ebau.sg.ch",
  allowApplicantManualWorkItem: false,
  documentBackend: "alexandria",
  showIdInInternalArea: false,
  instanceStates: {
    new: 1,
    subm: 2,
    rejected: 3,
    "init-distribution": 4,
    distribution: 5,
    decision: 6,
    decided: 7,
  },
  gwr: {
    cantonAbbreviation: "SG",
    importModels: ["project", "building", "dwelling"],
    modalContainer: "body",
  },
  submittedStates: [],
  answerSlugs: {
    objectStreet: "strasse-und-nr",
    objectZIP: "plz",
    objectLocation: "ort",
    description: "beschreibung-bauvorhaben",
    municipality: "gemeinde",
    specialId: "dossier-number",
    parcel: "parzellen",
    parcelNumber: "parzellennummer",
    buildingLawNumber: "baurecht-nummer",
    firstNameApplicant: "vorname",
    lastNameApplicant: "name",
    juristicNameApplicant: "juristische-person-name",
    isJuristicApplicant: "juristische-person",
    isJuristicApplicantYes: "juristische-person-ja",
    personalDataApplicant: "gesuchstellerin",
  },
  personalSuggestions: {
    tableQuestions: ["gesuchstellerin"],
    firstNameRegexp: "^vorname$",
    lastNameRegexp: "^name$",
    juristicNameRegexp: "^juristische-person-name$",
    emailRegexp: "^e-mail$",
  },
  intentSlugs: ["beschreibung-bauvorhaben"],
  submitComponent: {
    requiredPermissions: {
      submit: ["instance-submit"],
    },
    export: { enabled: () => false },
  },
  communication: {
    rolesWithApplicantContact: ["activeOrInolvedLeadAuthority", "service"],
  },
  rejection: {
    instanceState: "rejected",
    allowedInstanceStates: ["subm"],
  },
  publication: {
    public: {
      task: "fill-publication",
      createTask: "create-publication",
      dateRanges: [["publikation-start", "publikation-ende"]],
    },
  },
};

config.submittedStates = Object.entries(config.instanceStates)
  .filter(([name]) => name !== "new")
  .map(([, id]) => id);

export default config;
