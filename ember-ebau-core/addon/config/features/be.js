export default {
  publication: {
    showMainForm: true,
    endDate: false,
    related: true,
    disableAuthentication: false,
    showDocumentsInfo: true,
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
    snippets: true,
    revert: true,
  },
  cases: {
    directLinkToPortal: true,
    createPaper: true,
    exportExcel: true,
    downloadFormAsPdf: true,
  },
  servicePermissions: {
    hasConstructionControl: true,
  },
  gis: {
    v3: true,
    showChanges: true,
  },
  communications: {
    enabled: true,
    snippets: true,
  },
  portal: {
    stateInfoButton: true,
  },
  dashboard: {
    useLegacy: false,
  },
  corrections: {
    archiveInstance: true,
    copyInstance: true,
    changeDossierNumber: true,
    changeForm: true,
    convertModification: true,
    correctForm: true,
    withdrawInstance: false,
  },
  changeGeometer: {
    enabled: true,
  },
  additionalDemands: {
    enabled: true,
    showAuthor: true,
    showMigrated: true,
  },
  workItems: {
    v2: true,
  },
  support: true,
  staticFaq: true,
  modificationConfirm: true,
  instanceSupport: true,
};
