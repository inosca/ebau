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
      default: [
        "form",
        "dossierNumber",
        "address",
        "parcel",
        "personalDetails",
        "intent",
        "submitDateAfter",
        "submitDateBefore",
        "keywords",
        "instanceState",
        "responsibleServiceUser",
      ],
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
  personalDetailsSlugs: [
    answerSlugs.juristicNameApplicant,
    answerSlugs.firstNameApplicant,
    answerSlugs.lastNameApplicant,
  ],
};
