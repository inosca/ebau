export default {
  publication: {
    showMainForm: true,
    endDate: false,
    related: true,
    disableAuthentication: false,
  },
  billing: {
    charge: false,
    organization: false,
    reducedTaxRate: true,
    orderTaxByRate: false,
    displayService: false,
    billingType: false,
    legalBasis: false,
    costCenter: false,
  },
  rejection: {
    useLegacyClaims: true,
    snippets: true,
    revert: true,
  },
  cases: {
    createPaper: true,
    exportExcel: true,
    downloadFormAsPdf: true,
  },
  servicePermissions: {
    hasConstructionControl: true,
  },
  gis: {
    v3: true,
  },
  communications: {
    enabled: true,
    snippets: true,
  },
  portal: {
    stateInfoButton: true,
  },
  dashboard: {
    useLegacy: true,
  },
  submitComponent: {
    requiredPermissions: ["instance-submit"],
    buttonHintEnabled: (session) => session.isSupport,
    export: {
      enabled: (instance) => !instance.isPaper,
      templateName: () => `form`,
      errorMessage: "dms.downloadError",
      customFormSlugs: ["sb1", "sb1-v2", "sb2"],
    },
  },
  corrections: {
    archiveInstance: true,
    changeDossierNumber: true,
    changeForm: true,
    convertModification: true,
    correctForm: true,
    withdrawInstance: false,
  },
};
