export default {
  columns: {
    caluma: {
      service: [
        "instanceId",
        "dossierNumber",
        "form",
        "address",
        "inquiryCreated",
        "instanceState",
        "intent",
        "applicants",
      ],
      default: [
        "instanceId",
        "dossierNumber",
        "form",
        "address",
        "submitDate",
        "instanceState",
        "intent",
        "applicants",
      ],
    },
  },
  activeFilters: {
    caluma: {
      service: [
        "form",
        "instanceId",
        "dossierNumber",
        "municipality",
        "responsibleMunicipality",
        "responsibleServiceUser",
        "address",
        "parcel",
        "personalDetails",
        "intent",
        "inquiryState",
        "inquiryAnswer",
        "inquiryCreatedAfter",
        "inquiryCreatedBefore",
        "inquiryCompletedAfter",
        "inquiryCompletedBefore",
        "tags",
        "instanceState",
        "paper",
      ],
      municipality: [
        "form",
        "instanceId",
        "dossierNumber",
        "municipality",
        "responsibleServiceUser",
        "address",
        "parcel",
        "personalDetails",
        "intent",
        "submitDateAfter",
        "submitDateBefore",
        "tags",
        "instanceState",
        "decision",
        "paper",
      ],
      default: [
        "form",
        "instanceId",
        "dossierNumber",
        "municipality",
        "responsibleMunicipality",
        "address",
        "personalDetails",
        "instanceState",
      ],
    },
  },
  filterPresets: {
    service: {
      pending: { instanceState: ["20004"], inquiryState: "pending" },
      paper: { paper: "1" },
    },
    municipality: {
      paper: { paper: "1" },
    },
  },
  availableOrderings: {
    instanceId: {
      caluma: [{ meta: "camac-instance-id" }],
    },
    submitDate: {
      caluma: [{ meta: "submit-date" }],
    },
  },
  defaultOrder: "instanceId",
};