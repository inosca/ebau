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
    creationActivatedForEchApiUsers: false,
  },
  deadlines: {
    enabled: true,
    useEndDate: false,
    manualSuspensionReason: false,
  },
  permissions: {
    applicantRoles: true,
  },
  rejection: {
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
  instanceMarks: true,
  instanceOverview: {
    useFormNameAsTabTitle: true,
  },
  snippets: {
    journal: true,
    workItems: true,
    rejection: true,
    billing: true,
    communications: true,
    deadlines: true,
  },
};
