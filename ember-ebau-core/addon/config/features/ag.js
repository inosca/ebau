import { getOwnConfig, isDevelopingApp } from "@embroider/macros";

export default {
  billing: {
    charge: true,
    reducedTaxRate: true,
    displayService: true,
  },
  communications: {
    enabled: true,
  },
  permissions: {
    applicantRoles: true,
  },
  rejection: {
    useLegacyClaims: false,
    snippets: false,
    revert: true,
  },
  watermark: isDevelopingApp() || getOwnConfig().enableWatermark,
};
