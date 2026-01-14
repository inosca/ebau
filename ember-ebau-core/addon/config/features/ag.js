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
  deadlines: {
    enabled: true,
    useEndDate: false,
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
  additionalDemands: {
    enabled: true,
  },
  publication: {
    showMainForm: true,
  },
  corrections: {
    archiveInstance: false,
    changeDossierNumber: false,
    changeForm: true,
    convertModification: false,
    correctForm: true,
    withdrawInstance: true,
  },
  internalCaseCreation: true,
  cases: {
    exportExcel: true,
    showNoApplicantRegisteredWarning: true,
  },
  dms: {
    hideDownloadButton: true,
  },
  profile: {
    enabled: true,
    showDivision: false,
  },
  organisation: {
    department: true,
  },
  submitComponent: {
    requiredPermissions: null,
  },
  workItems: {
    cancel: true,
    v2: true,
  },
  withdrawal: {
    light: true,
  },
  distribution: {
    deadlineRules: true,
  },
  changeGeometer: {
    enabled: false,
  },
};
