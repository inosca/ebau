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
    useLegacyClaims: false,
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
  submitComponent: {
    requiredPermissions: null,
    export: {
      enabled: (instance) =>
        !instance.isPaper &&
        !instance.calumaForm.startsWith("vorlaeufige-beurteilung"),
      templateName: (locale) => `eingabequittung-${locale}`,
      errorMessage: "dms.downloadError",
    },
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
  },
  changeGeometer: {
    enabled: false,
  },
};
