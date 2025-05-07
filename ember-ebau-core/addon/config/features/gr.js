import { getOwnConfig, isDevelopingApp } from "@embroider/macros";

export default {
  publication: {
    showMainForm: true,
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
  additionalDemands: true,
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
};
