import { getOwnConfig, isDevelopingApp } from "@embroider/macros";

export default {
  billing: {
    charge: true,
    reducedTaxRate: true,
    displayService: true,
    applyConstructionCosts: true,
    remark: true,
    snippets: true,
  },
  communications: {
    enabled: true,
    snippets: true,
    creationActivatedForEchApiUsers: false,
  },
  deadlines: {
    enabled: true,
    useEndDate: false,
    manualSuspensionReason: false,
    snippets: true,
  },
  permissions: {
    applicantRoles: true,
  },
  rejection: {
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
    copyInstance: false,
    changeDossierNumber: false,
    changeForm: true,
    convertModification: false,
    correctForm: true,
    withdrawInstance: false,
    deleteInternalInstance: true,
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
  workItems: {
    cancel: true,
    v2: true,
    snippets: true,
  },
  withdrawal: {
    light: true,
  },
  distribution: {
    deadlineRules: true,
    showAllServices: true,
  },
  changeGeometer: {
    enabled: false,
  },
  gis: {
    v3: true,
  },
  support: true,
  staticFaq: true,
  instanceSupport: true,
  journal: {
    snippets: true,
  },
  instanceMarks: true,
};
