import { getOwnConfig, isDevelopingApp } from "@embroider/macros";

export default {
  watermark: isDevelopingApp() || getOwnConfig().enableWatermark,
  permissions: {
    applicantRoles: true,
  },
  workItems: {
    v2: true,
    snippets: true,
  },
  instanceOverview: {
    useSpecialId: true,
    useFormNameAsTabTitle: true,
  },
  communications: {
    enabled: true,
    snippets: true,
  },
  rejection: {
    revert: true,
    snippets: true,
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
  journal: {
    snippets: true,
  },
  billing: {
    snippets: true,
  },
  deadlines: {
    snippets: true,
  },
  form: {
    extraWide: true,
  },
};
