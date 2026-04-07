export default {
  name: "ag",
  languages: ["de"],
  fallbackLanguage: "de",
  prodUrl: "diba.ag.ch",
  allowApplicantManualWorkItem: false,
  documentBackend: "alexandria",
  showIdInInternalArea: false,
  serviceGroups: {
    afb: 4,
  },
  instanceStates: {
    new: 1,
    subm: 120004,
    circulation: 120005,
    decision: 120007,
    correction: 120008,
    "init-distribution": 120009,
    rejected: 120011,
  },
  gwr: {
    cantonAbbreviation: "AG",
    importModels: ["project", "building", "dwelling"],
    modalContainer: "body",
  },
  submittedStates: [
    120004, // subm
    120005, // circulation
    120006, // finished
    120007, // decision
    120008, // correction
    120009, // init-distribution
    120010, // construction-acceptance
    120011, // rejected
  ],
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
    hasRepresentativeApplicant: "vertretung-gesuchstellerin",
    hasRepresentativeApplicantYes: "vertretung-gesuchstellerin-ja",
    personalDataApplicant: "personalien-gesuchstellerin",
    coordinates: "gis-map",
    evenProjectNumber: "projektkennzeichnung-even",
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
      createTask: "create-publication",
      dateRanges: [
        [
          "beginn-publikationsorgan-gemeinde",
          "ende-publikationsorgan-gemeinde",
        ],
        [
          "beginn-publikation-kantonsamtsblatt",
          "ende-publikation-kantonsamtsblatt",
        ],
      ],
    },
    neighbors: {
      task: "fill-information-of-neighbors",
      createTask: "create-information-of-neighbors",
      dateRanges: [
        [
          "nachbarschaftsorientierung-beginn",
          "nachbarschaftsorientierung-ende",
        ],
      ],
    },
  },
  decision: {
    task: "decision",
    answerSlugs: {
      decision: "entscheid-entscheid",
      remarks: "entscheid-bemerkungen",
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
  rejection: {
    instanceState: "rejected",
    allowedInstanceStates: [
      "subm",
      "init-distribution",
      "circulation",
      "decision",
    ],
  },
  alexandria: {
    feedbackCategories: ["alle-beteiligten", "bauabnahme"],
    marks: {
      decision: "decision",
      void: "void",
    },
  },
  showDownloadReceiptAction: true,
  customDeadlineServiceGroupSlugs: ["service-afb"],
  customDeadlineServiceSlugs: [
    "agv-bs",
    "agv-esp",
    "bks-dp",
    "bks-ka",
    "dvi-awa-iga",
    "amb",
    "aew",
    "axpo",
    "dgs-avs-vet",
    "dgs-avs-lmi",
  ],
  communication: {
    rolesWithApplicantContact: ["activeOrInolvedLeadAuthority", "service"],
  },
  dossierImport: {
    municipalityAdminRole: 5, // Administration Gemeinde
    municipalityServiceGroup: 2, // Gemeinde
  },
  modification: {
    allowForms: ["baugesuch"],
    disallowStates: ["new"],
  },
  legalSubmission: {
    task: "objections",
    tableForm: "einwendung",
    tableQuestion: "einwendungen",
    orderQuestion: "einwendung-datum",
    columns: {
      date: "einwendung-datum",
      "legal-claimants": "einwendung-einwendende",
      withdrawn: "einwendung-zurueckgezogen",
      "has-representative": "einwendung-einwendende",
    },
  },
  displayedForms: [
    {
      section: "paper-instances",
      forms: [
        {
          slug: "baugesuch",
          roles: ["municipality-lead", "municipality-clerk"],
          serviceGroups: ["municipality", "municipality-light"],
          category: "building-permit",
        },
        {
          slug: "baugesuch-mit-uvp",
          roles: ["municipality-lead", "municipality-clerk"],
          serviceGroups: ["municipality", "municipality-light"],
          category: "building-permit",
        },
        {
          slug: "vorentscheid",
          roles: ["municipality-lead", "municipality-clerk"],
          serviceGroups: ["municipality", "municipality-light"],
          category: "building-permit",
        },
        {
          slug: "anfrage",
          roles: ["municipality-lead", "municipality-clerk"],
          serviceGroups: ["municipality", "municipality-light"],
          category: "special-procedure",
        },
        {
          slug: "reklame",
          roles: ["municipality-lead", "municipality-clerk"],
          serviceGroups: ["municipality", "municipality-light"],
          category: "special-procedure",
        },
      ],
    },
    {
      section: "internal-dossiers",
      forms: [
        {
          slug: "anfrage-intern",
          roles: [
            "municipality-lead",
            "municipality-clerk",
            "trusted-service-lead",
            "trusted-service-clerk",
          ],
          serviceGroups: ["municipality", "service-afb"],
          category: "special-procedure",
        },
        {
          slug: "internes-dossier",
          roles: [
            "municipality-lead",
            "municipality-clerk",
            "trusted-service-lead",
            "trusted-service-clerk",
          ],
          serviceGroups: ["municipality", "service-afb"],
          category: "special-procedure",
        },
      ],
    },
    {
      section: "special-procedure",
      forms: [
        {
          slug: "plangenehmigungsverfahren-bund",
          roles: ["municipality-lead", "municipality-clerk"],
          serviceGroups: ["authority-pgv"],
        },
        {
          slug: "plangenehmigungsverfahren-gas",
          roles: ["municipality-lead", "municipality-clerk"],
          serviceGroups: ["authority-pgv"],
        },
      ],
    },
  ],
  submitComponent: {
    requiredPermissions: {
      submit: ["instance-submit"],
    },
  },
};
