export default {
  publication: {
    form: true,
    endDate: false,
    related: true,
    disableAuthentication: false,
  },
  billing: {
    charge: false,
    organization: false,
    reducedTaxRate: false,
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
  communication: {
    snippets: true,
  },
  cases: {
    createPaper: true,
    exportExcel: true,
  },
  servicePermissions: {
    hasConstructionControl: true,
  },
  gis: {
    v3: true,
  },
  communications: true,
};
