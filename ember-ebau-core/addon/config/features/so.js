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
    useLegacyClaims: false,
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
  },
  watermark: isDevelopingApp() || getOwnConfig().enableWatermark,
  municipalityLogo: true,
  communications: {
    enabled: true,
  },
  constructionMonitoring: true,
  additionalDemands: true,
  submitComponent: {
    requiredPermissions: ["instance-submit"],
    export: {
      enabled: (instance) =>
        !instance.isPaper && instance.calumaForm !== "voranfrage",
      templateName: () => `signatures`,
    },
  },
  corrections: {
    archiveInstance: false,
    changeDossierNumber: false,
    changeForm: false,
    convertModification: false,
    correctForm: true,
    withdrawInstance: true,
  },
};
