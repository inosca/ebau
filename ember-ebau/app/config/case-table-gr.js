export default {
  columns: {
    caluma: [
      "instanceId",
      "ebauNr",
      "caseDocumentFormName",
      "intent",
      "instanceState",
    ],
  },
  activeFilters: {
    caluma: ["dossierNumber", "intent", "caseStatus", "caseDocumentFormName"],
  },
  order: [{ meta: "dossier-number" }],
};
