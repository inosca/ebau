import { getOwnConfig, isDevelopingApp } from "@embroider/macros";

export default {
  billing: {
    charge: true,
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
