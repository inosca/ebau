import { getOwnConfig, isDevelopingApp } from "@embroider/macros";

export default {
  watermark: isDevelopingApp() || getOwnConfig().enableWatermark,
  permissions: {
    applicantRoles: true,
  },
  workItems: {
    v2: true,
  },
  instanceOverview: {
    showInternalStatus: true,
    statusTimeline: true,
  },
  communications: {
    enabled: true,
  },
  rejection: {
    revert: true,
  },
  alexandria: {
    showSearchLinkLabel: true,
  },
  publication: {
    showMainForm: true,
  },
  gis: {
    v3: true,
    showChanges: true,
  },
  distribution: {
    showAllServices: true,
    fourEyesPrinciple: true,
  },
  instanceMarks: true,
  dms: {
    enableSystemTemplateEditing: true,
  },
  billing: {
    charge: true,
    reducedTaxRate: true,
    displayService: true,
    applyConstructionCosts: true,
    remark: true,
  },
  form: {
    extraWide: true,
  },
  withdrawal: {
    light: true,
  },
  snippets: {
    allowGlobalSnippets: true,
    deadlines: true,
    billing: true,
    journal: true,
    rejection: true,
    communications: true,
    workItems: true,
  },
};
