import { getOwnConfig, isDevelopingApp } from "@embroider/macros";

export default {
  publication: {
    form: true,
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
  },
  permissions: {
    municipalityBeforeSubmission: true,
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
  communications: true,
  constructionMonitoring: true,
};
