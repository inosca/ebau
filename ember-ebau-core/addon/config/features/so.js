import { getOwnConfig, isDevelopingApp } from "@embroider/macros";

export default {
  publication: {
    showMainForm: true,
    endDate: false,
    related: false,
    disableAuthentication: false,
  },
  billing: {
    charge: false,
    organization: true,
    reducedTaxRate: true,
    orderTaxByRate: false,
    displayService: true,
    billingType: true,
    legalBasis: true,
    costCenter: true,
  },
  rejection: {
    snippets: false,
    revert: false,
  },
  cases: {
    createPaper: true,
    exportExcel: false,
    downloadFormAsPdf: true,
  },
  permissions: {
    municipalityBeforeSubmission: true,
    applicantRoles: true,
  },
  caluma: {
    useNumberSeparatorWidgetAsDefault: true,
  },
  gis: {
    showChanges: true,
  },
  login: {
    tokenExchange: getOwnConfig().enableTokenExchange,
  },
  dms: {
    hideDownloadButton: true,
  },
  instanceOverview: {
    useSpecialId: true,
    hideActionDescription: true,
  },
  watermark: isDevelopingApp() || getOwnConfig().enableWatermark,
  municipalityLogo: true,
  communications: {
    enabled: true,
  },
  constructionMonitoring: true,
  additionalDemands: {
    enabled: true,
  },
  corrections: {
    archiveInstance: false,
    copyInstance: false,
    changeDossierNumber: false,
    changeForm: false,
    convertModification: false,
    correctForm: true,
    withdrawInstance: true,
  },
  profile: {
    enabled: true,
    showDivision: true,
  },
  workItems: {
    hideImportedWorkItems: true,
    v2: true,
  },
  changeGeometer: {
    enabled: false,
  },
  instanceHeader: {
    shortIntent: true,
    staticKeywords: true,
  },
  deadlines: {
    enabled: false,
    useEndDate: true,
  },
};
