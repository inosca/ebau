import { getOwnConfig, isDevelopingApp } from "@embroider/macros";

export default {
  publication: {
    form: false,
    endDate: true,
    related: false,
    disableAuthentication: true,
    showPrintButton: true,
  },
  rejection: {
    revert: true,
  },
  constructionMonitoring: true,
  communications: {
    enabled: true,
  },
  additionalDemands: {
    enabled: true,
  },
  workItems: {
    showDocument: true,
    v2: true,
    showTaskFilter: true,
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
  instancePaperFilterDefault: true,
};
