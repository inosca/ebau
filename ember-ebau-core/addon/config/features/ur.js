import { getOwnConfig, isDevelopingApp } from "@embroider/macros";

export default {
  publication: {
    form: false,
    endDate: true,
    related: false,
    disableAuthentication: true,
  },
  rejection: {
    revert: true,
  },
  constructionMonitoring: true,
  additionalDemands: {
    enabled: true,
  },
  workItems: {
    showDocument: true,
    v2: true,
  },
  dashboard: {
    useLegacy: true,
  },
  workItemList: {
    useExperimentalLayout: true,
    useColorForNFD: true,
  },
  watermark: isDevelopingApp() || getOwnConfig().enableWatermark,
  changeGeometer: {
    enabled: false,
  },
  support: true,
};
