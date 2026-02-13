import { getOwnConfig, isDevelopingApp } from "@embroider/macros";

export default {
  watermark: isDevelopingApp() || getOwnConfig().enableWatermark,
  permissions: {
    applicantRoles: true,
  },
  workItems: {
    v2: true,
  },
  instanceOverview: {
    useSpecialId: true,
  },
};
