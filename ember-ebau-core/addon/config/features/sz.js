export default {
  billing: {
    charge: true,
    organization: true,
    reducedTaxRate: true,
    orderTaxByRate: true,
    displayService: false,
    billingType: false,
    legalBasis: false,
    costCenter: false,
    releaseForClearing: {
      enabled: true,
      allowedForServiceGroups: ["baugesuchszentrale", "fachstellen"],
    },
    productNumber: true,
  },
  cases: {
    createPaper: false,
    exportExcel: true,
  },
  journal: {
    snippets: true,
  },
  constructionMonitoring: true,
  communications: {
    enabled: true,
    hideInstanceId: true,
    snippets: true,
  },
};
