import { getOwnConfig, isDevelopingApp } from "@embroider/macros";

export default {
  permissions: {
    applicantRoles: true,
  },
  watermark: isDevelopingApp() || getOwnConfig().enableWatermark,
};
