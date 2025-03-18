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
    // Set both to true once wilken is ready or for dev
    releaseForClearing: false,
    productNumber: false,
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
