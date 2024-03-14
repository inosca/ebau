import mainConfig from "ember-ebau-core/config/main";

const { answerSlugs } = mainConfig;

export default {
  columns: {
    caluma: {
      service: [
        "dossierNumber",
        "form",
        "address",
        "inquiryCreated",
        "instanceState",
        "intent",
        "applicants",
      ],
      default: [
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
        "dossierNumber",
        "municipality",
        // "responsibleServiceUser",
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
        "keywords",
        "instanceState",
        "paper",
      ],
      municipality: [
        "form",
        "dossierNumber",
        "municipality",
        // "responsibleServiceUser",
        "address",
        "parcel",
        "personalDetails",
        "intent",
        "submitDateAfter",
        "submitDateBefore",
        "keywords",
        "instanceState",
        "decision",
        "paper",
      ],
      default: [
        "form",
        "dossierNumber",
        "municipality",
        "address",
        "personalDetails",
        "intent",
        "submitDateAfter",
        "submitDateBefore",
        "keywords",
        "instanceState",
        "decision",
        "paper",
      ],
    },
  },
  filterPresets: {
    service: {
      paper: { paper: "1" },
    },
    municipality: {
      paper: { paper: "1" },
    },
  },
  availableOrderings: {
    dossierNumber: {
      caluma: [{ meta: `${answerSlugs.specialId}-sort` }],
    },
    submitDate: {
      caluma: [{ meta: "submit-date" }],
    },
  },
  defaultOrder: "dossierNumber",
  addressSlugs: [answerSlugs.objectStreet, answerSlugs.objectLocation],
  parcelSlugs: [answerSlugs.parcelNumber],
};
