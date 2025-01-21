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
  watermark: isDevelopingApp() || getOwnConfig().enableWatermark,
};
