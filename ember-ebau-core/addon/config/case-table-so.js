import mainConfig from "ember-ebau-core/config/main";

const { answerSlugs } = mainConfig;

export default {
  columns: {
    caluma: {
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
      municipality: [
        "form",
        "dossierNumber",
        "municipality",
        "address",
        "parcel",
        "personalDetails",
        "intent",
        "submitDateAfter",
        "submitDateBefore",
        "instanceState",
      ],
      default: [
        "form",
        "dossierNumber",
        "municipality",
        "address",
        "personalDetails",
        "instanceState",
      ],
    },
  },
  availableOrderings: {
    dossierNumber: {
      caluma: [{ meta: answerSlugs.specialId }],
    },
    submitDate: {
      caluma: [{ meta: "submit-date" }],
    },
  },
  defaultOrder: "dossierNumber",
  addressSlugs: [
    answerSlugs.objectStreet,
    answerSlugs.objectNumber,
    answerSlugs.objectLocation,
  ],
  parcelSlugs: [answerSlugs.parcelNumber],
};
