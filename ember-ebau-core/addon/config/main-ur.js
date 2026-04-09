export default {
  name: "ur",
  languages: ["de"],
  fallbackLanguage: "de",
  prodUrl: "urec.ur.ch",
  showInstanceIdAfterSubmission: true,
  documentBackend: "camac",
  showIdInInternalArea: true,
  gwr: {
    cantonAbbreviation: "UR",
    importModels: ["project", "building", "dwelling"],
  },
  allowApplicantManualWorkItem: false,
  journalDefaultVisibility: true,
  journalEntryDuration: false,
  allowedInstanceLinkingGroups: [
    142, // KOOR BG
    21, // KOOR NP
  ],
  useLocation: true,
  urGisUrl: "https://service-lv95.lisag.hosting.karten-werk.ch/wms?tiled=True",
  attachmentSections: {
    applicant: "12000000",
    internal: "12000001",
  },
  submittedStates: [
    21, // comm
    22, // ext
    23, // circ
    24, // redac
    25, // done
    26, // arch
    29, // nfd
    30, // subm
    31, // rejected
    32, // ext_gem
    33, // old
    34, // control
  ],
  answerSlugs: {
    objectStreet: "parcel-street",
    objectNumber: "street-number",
    objectLocation: "parcel-city",
    applicantZip: "zip",
    description: "proposal-description",
    municipality: "municipality",
    specialId: "dossier-number",
    parcel: "parcels",
    parcelNumber: "parcel-number",
    oerebProcedure: "typ-des-verfahrens",
    oerebTopicsCanton: "oereb-thema",
    oerebPartialState: "teilstatus",
    procedureCanton: "mbv-type",
    procedureConfederation: "mbv-bund-type",
    staticForestBoundaryCanton:
      "waldfeststellung-mit-statischen-waldgrenzen-kanton",
    staticForestBoundaryMunicipality:
      "waldfeststellung-mit-statischen-waldgrenzen-gemeinde",
    personalDataApplicant: "applicant",
    firstNameApplicant: "first-name",
    lastNameApplicant: "last-name",
    juristicNameApplicant: "juristic-person-name",
  },
  personalSuggestions: {
    tableQuestions: [
      "applicant",
      "landowner",
      "project-author",
      "invoice-recipient",
    ],
    firstNameRegexp: "^first-name$",
    lastNameRegexp: "^last-name$",
    juristicNameRegexp: "^juristic-person-name$",
    emailRegexp: "^e-mail$",
  },
  paperInstances: {
    allowedGroups: {
      roles: [
        6, // Sekretariat der Gemeindebaubehörde
        3, // KOOR BG
        1061, // KOOR NP
        1101, // KOOR BD
        1106, // KOOR AfU
        1107, // KOOR ALA
        1127, // KOOR AfE
        1128, // KOOR AFJ
        1129, // KOOR SD
        1133, // KOOR AfG
        1130, // Bundesstelle
        1131, // Support
      ],
      serviceGroups: [
        1, // Koordinationsstellen
        68, // Sekretariate Gemeindebaubehörden
        70, // Bundesstellen
      ],
    },
  },
  publication: {
    public: {
      task: "fill-publication",
      createTask: "create-publication",
      dateRanges: [
        ["publikation-publikationsbeginn", "publikation-publikationsende"],
      ],
    },
  },
  instanceResourceRedirects: {
    journal: 14000014,
    form: 14000012,
  },
  intentSlugs: [
    "proposal-description",
    "beschreibung-zu-mbv",
    "bezeichnung",
    "vorhaben-proposal-description",
    "veranstaltung-beschrieb",
    "beschreibung-reklame",
    "beschrieb-verfahren",
  ],
  customDeadlineServiceGroupSlugs: ["Koordinationsstellen"],
  constructionMonitoring: {
    instanceStates: ["control"],
  },
  instanceStates: {
    new: 28,
    finished: 25, // done
    archived: 26, // arch
    rejected: 31,
    old: 33,
    control: 34,
    comm: 21,
  },
  modification: {
    allowForms: ["building-permit"],
    disallowStates: ["new", "archived", "finished", "old"],
  },
  rejection: {
    instanceState: "rejected",
    allowedInstanceStates: ["comm", "circ", "done", "control"],
  },
  trustedServiceRole: 4,
  submitComponent: {
    requiredPermissions: {
      submit: ["instance-submit"],
    },
  },
  oerebPublicationMapping: {
    "oereb-thema-bausperre": "bausperre",
    "oereb-thema-schutzmassnahmen": "schutzmassnahmen",
    "oereb-thema-grundwasserschutz": "planerischerGewaesserschutz",
    "oereb-thema-kpz": "kantonalePlanungszone",
    "oereb-thema-knp": "kantonaleNutzungsplanung",
    "oereb-thema-kantonale-baulinien": "kantonaleBaulinie",
    "oereb-thema-gpz": "gemeindlichePlanungszone",
    "oereb-thema-snp-bl-gemeinde": "gemeindlicheBaulinie",
    "oereb-thema-snp-qgp-qp": "sondernutzungsplanung",
    "oereb-thema-war": "schutzmassnahmen",
    "oereb-thema-gnp": "gemeindlicheNutzungsplanung",
  },
  publicationTemplateMapping: {
    baubewilligung: "publish-print-bg",
    bausperre: "publish-print-bausperre",
    schutzmassnahmen: "publish-print-sm",
    gewaesserschutzbereich: "publish-print-pg",
    kantonalePlanungszone: "publish-print-kpz",
    kantonaleNutzungsplanung: "publish-print-knp",
    kantonaleBaulinie: "publish-print-kbl",
    gemeindlichePlanungszone: "publish-print-gnp",
    gemeindlicheBaulinie: "publish-print-gbl",
    sondernutzungsplanung: "publish-print-snp",
  },
  remarkMapping: {
    "publikation-bemerkungen-profilierung-auf-verlangen":
      "Profilierung auf Verlangen",
    "publikation-bemerkungen-profiliert": "Profiliert",
    "publikation-bemerkungen-verpflockt": "Verpflockt",
    "publikation-bemerkungen-keine-profilierung": "Keine Profilierung",
  },
};
