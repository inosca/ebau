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
  communications: {
    enabled: true,
  },
  rejection: {
    revert: true,
  },
  alexandria: {
    showSearchLinkLabel: true,
  },
  publication: {
    showMainForm: true,
  },
};
