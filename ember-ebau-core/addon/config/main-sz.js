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
  answerSlugs: {},
  communication: {
    rolesWithApplicantContact: ["activeOrInolvedLeadAuthority"],
  },
};
