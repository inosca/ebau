import { getOwnConfig, isDevelopingApp } from "@embroider/macros";

export default {
  billing: {
    charge: true,
    reducedTaxRate: true,
    displayService: true,
    applyConstructionCosts: true,
  },
  communications: {
    enabled: true,
    snippets: true,
  },
  permissions: {
    applicantRoles: true,
  },
  rejection: {
    useLegacyClaims: false,
    snippets: true,
    revert: true,
  },
  watermark: isDevelopingApp() || getOwnConfig().enableWatermark,
  additionalDemands: true,
  publication: {
    showMainForm: true,
  },
};
