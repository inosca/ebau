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
  additionalDemands: true,
  workItems: {
    showDocument: true,
  },
  dashboard: {
    useLegacy: true,
  },
  workItemList: {
    useExperimentalLayout: true,
    useColorForNFD: true,
  },
  watermark: isDevelopingApp() || getOwnConfig().enableWatermark,
  submitComponent: {
    requiredPermissions: ["instance-submit"],
  },
};
