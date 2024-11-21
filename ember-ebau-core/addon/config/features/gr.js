import { getOwnConfig, isDevelopingApp } from "@embroider/macros";

export default {
  publication: {
    form: true,
    endDate: false,
    related: false,
    disableAuthentication: false,
  },
  rejection: {
    useLegacyClaims: false,
    snippets: false,
    revert: true,
  },
  cases: {
    createPaper: true,
    exportExcel: false,
  },
  permissions: {
    applicantRoles: true,
  },
  caluma: {
    useNumberSeparatorWidgetAsDefault: true,
  },
  watermark: isDevelopingApp() || getOwnConfig().enableWatermark,
  communications: true,
  additionalDemands: true,
  dashboard: {
    useLegacy: true,
  },
  workItemList: {
    useExperimentalLayout: true,
  },
};
