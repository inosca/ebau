import { getOwnConfig, isDevelopingApp } from "@embroider/macros";

export default {
  publication: {
    showMainForm: true,
    endDate: false,
    related: false,
    disableAuthentication: true,
    useCaptchaAuthentication: true,
  },
  rejection: {
    snippets: false,
    revert: true,
  },
  cases: {
    createPaper: true,
    exportExcel: false,
    downloadFormAsPdf: true,
  },
  permissions: {
    applicantRoles: true,
  },
  caluma: {
    useNumberSeparatorWidgetAsDefault: true,
  },
  watermark: isDevelopingApp() || getOwnConfig().enableWatermark,
  communications: {
    enabled: true,
  },
  deadlines: {
    enabled: true,
    useEndDate: true,
  },
  additionalDemands: {
    enabled: true,
  },
  dashboard: {
    useLegacy: true,
  },
  workItemList: {
    useExperimentalLayout: true,
  },
  corrections: {
    archiveInstance: false,
    changeDossierNumber: false,
    changeForm: false,
    convertModification: false,
    correctForm: true,
    withdrawInstance: true,
  },
  workItems: {
    v2: true,
    targetDeadlineDate: true,
  },
  changeGeometer: {
    enabled: false,
  },
  support: true,
  showProfileLink: true,
  instanceSupport: true,
};
