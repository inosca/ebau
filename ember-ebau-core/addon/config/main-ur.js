export default {
  name: "ur",
  languages: ["de"],
  fallbackLanguage: "de",
  prodUrl: "urec.ur.ch",
  showInstanceIdAfterSubmission: true,
  documentBackend: "camac",
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
  urGisUrl: "https://geo.ur.ch/wms",
  attachmentSections: { applicant: "12000000", internal: "12000001" },
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
    parcelNumber: "parcel-number",
    oerebProcedure: "typ-des-verfahrens",
    oerebTopicsCanton: "oereb-thema",
    oerebTopicsMunicipality: "oereb-thema-gemeinde",
    oerebPartialState: "teilstatus",
    procedureCanton: "mbv-type",
    procedureConfederation: "mbv-bund-type",
    staticForestBoundaryCanton:
      "waldfeststellung-mit-statischen-waldgrenzen-kanton",
    staticForestBoundaryMunicipality:
      "waldfeststellung-mit-statischen-waldgrenzen-gemeinde",
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
  instanceResourceRedirects: {
    journal: {
      3: 772, // KOOR BG
      1101: 12000005, // KOOR BD
      1127: 12000007, // KOOR AfE
      1128: 12000009, // KOOR AFJ
      1107: 12000006, // KOOR ALA
      1061: 12000004, // KOOR NP
      1129: 12000009, // KOOR SD
      1106: 12000008, // KOOR AfU
      6: 20001, // Municipality
      1102: 12000001, // Gemeinde als Vernehmlassungsstelle
      4: 12000001, // Vernehmlassungsstelle mit Koordinationsaufgaben
      1021: 12000001, // Vernehmlassungsstelle ohne Koordinationsaufgaben
    },
    form: {
      3: 4, // KOOR BG
      1101: 605, // KOOR BD
      1127: 723, // KOOR AfE
      1128: 735, // KOOR AFJ
      1107: 714, // KOOR ALA
      1061: 445, // KOOR NP
      1129: 735, // KOOR SD
      1106: 699, // KOOR AfU
      6: 771, // Municipality
      1102: 2000000, // Gemeinde als Vernehmlassungsstelle
      4: 2000000, // Vernehmlassungsstelle mit Koordinationsaufgaben
      1021: 2000000, // Vernehmlassungsstelle ohne Koordinationsaufgaben
    },
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
};
