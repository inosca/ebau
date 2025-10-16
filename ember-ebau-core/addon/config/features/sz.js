export default {
  billing: {
    charge: true,
    organization: true,
    reducedTaxRate: true,
    orderTaxByRate: true,
    displayService: false,
    billingType: false,
    legalBasis: false,
    costCenter: false,
    // Keep this config in sync with django/camac/settings/modules/billing.py
    releaseForClearing: {
      enabled: true,
      forms: [
        "baugesuch-reklamegesuch",
        "projektanderung",
        "vorentscheid-gemass-ss84-pbg",
        "technische-bewilligung",
      ],
      allowedForServiceGroups: ["baugesuchszentrale", "fachstellen"],
      subsequentChargeAllowedForServices: [
        "baugesuchszentrale",
        "amfz-brandschutz",
        "afg-wasserbau",
        "afg-fischerei",
        "afg-industrie-gewerbeabwasser",
        "afg-entwaesserung",
      ],
    },
    productNumber: true,
  },
  cases: {
    createPaper: false,
    exportExcel: true,
  },
  journal: {
    snippets: true,
  },
  constructionMonitoring: true,
  communications: {
    enabled: true,
    hideInstanceId: true,
    snippets: true,
  },
  changeGeometer: {
    enabled: false,
  },
};
