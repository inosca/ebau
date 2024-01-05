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
  dms: {
    mergeAndSave: true,
  },
  index: {
    publicInstances: true,
  },
};
