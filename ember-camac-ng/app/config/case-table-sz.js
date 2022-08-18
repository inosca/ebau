export default {
  columns: {
    caluma: ["dossierNumber", "caseDocumentFormName", "intent", "caseStatus"],
    "camac-ng": [
      "dossierNumber",
      "instanceFormDescription",
      "location",
      "builder",
      "intentSZ",
      "instanceStateDescription",
    ],
  },
  activeFilters: {
    caluma: ["dossierNumber", "intent", "caseStatus", "form"],
    "camac-ng": [
      "instanceIdentifier",
      "municipality",
      "instanceState",
      "responsibleServiceUser",
      "address",
      "intent",
      "parcel",
      "builder",
      "landowner",
      "applicant",
      "submitDateAfter",
      "submitDateBefore",
      "service",
      "type",
    ],
  },
  formFields: [
    "bauherrschaft",
    "bauherrschaft-v2",
    "bauherrschaft-v3",
    "bauherrschaft-override",
    "bezeichnung",
    "bezeichnung-override",
  ],
  availableOrderings: {
    dossierNumber: {
      caluma: [{ meta: "dossier-number" }],
      "camac-ng": ["instance__identifier"],
    },
    caseStatus: {
      caluma: [{ attribute: "STATUS" }],
    },
    instanceStateDescription: {
      "camac-ng": ["instance__instance_state__description"],
    },
  },
  defaultOrder: "dossierNumber",
};
