export default {
  name: "sz",
  languages: ["de"],
  fallbackLanguage: "de",
  prodUrl: "behoerden.ebau-sz.ch",
  documentBackend: "camac",
  showIdInInternalArea: false,
  gwr: {
    cantonAbbreviation: "SZ",
    importModels: ["project", "building", "dwelling"],
  },
  allowApplicantManualWorkItem: true,
  journalDefaultVisibility: false,
  journalEntryDuration: true,
  newCase: {
    calumaWorkflow: "internal-document",
    camacForm: 11,
  },
  externalServiceGroupIds: [],
  useLocation: true,
  intentSlugs: ["voranfrage-vorhaben", "are-geschaeft-vorhaben"],
  answerSlugs: {
    specialId: "dossier-number",
  },
  communication: {
    rolesWithApplicantContact: ["activeOrInolvedLeadAuthority"],
  },
  servicePermissions: {
    includeSubRoutes: ["organisation"],
  },
  attachmentSections: {
    internal: 7,
  },
  // Keep this config in sync with django/camac/settings/modules/billing.py
  billing: {
    releaseForClearing: {
      forms: [
        "baugesuch-reklamegesuch",
        "projektanderung",
        "vorentscheid-gemass-ss84-pbg",
        "technische-bewilligung",
      ],
      allowedForServiceGroups: ["baugesuchszentrale", "fachstellen"],
      subsequentChargeAllowedForServices: [
        "baugesuchszentrale",
        "amfz-brandschutz",
        "afg-wasserbau",
        "afg-fischerei",
        "afg-industrie-gewerbeabwasser",
        "afg-entwaesserung",
      ],
    },
  },
};
