import { getOwnConfig, isDevelopingApp } from "@embroider/macros";

export default {
  billing: {
    charge: true,
    reducedTaxRate: true,
    displayService: true,
    applyConstructionCosts: true,
    remark: true,
  },
  communications: {
    enabled: true,
    snippets: true,
  },
  permissions: {
    applicantRoles: true,
  },
  rejection: {
    useLegacyClaims: false,
    snippets: true,
    revert: true,
  },
  watermark: isDevelopingApp() || getOwnConfig().enableWatermark,
  additionalDemands: true,
  publication: {
    showMainForm: true,
  },
  corrections: {
    changeForm: true,
  },
  internalCaseCreation: true,
  dms: {
    hideDownloadButton: true,
  },
  profile: true,
  organisation: {
    department: true,
  },
  submitComponent: {
    requiredPermissions: null,
    export: {
      enabled: (instance) => !instance.isPaper,
      templateName: (locale) => `eingabequittung-${locale}`,
    },
  },
};
