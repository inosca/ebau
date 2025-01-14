import { getOwnConfig, isDevelopingApp } from "@embroider/macros";

export default {
  communications: {
    enabled: true,
  },
  permissions: {
    applicantRoles: true,
  },
  watermark: isDevelopingApp() || getOwnConfig().enableWatermark,
};
