import mainConfig from "ember-ebau-core/config/main";

const { answerSlugs } = mainConfig;

export default {
  columns: {
    caluma: {
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
      default: [
        "form",
        "instanceId",
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
    instanceId: {
      caluma: [{ meta: "camac-instance-id" }],
    },
    dossierNumber: {
      caluma: [{ meta: `${answerSlugs.specialId}-sort` }],
    },
    submitDate: {
      caluma: [{ meta: "submit-date" }],
    },
  },
  defaultOrder: "dossierNumber",
  parcelSlugs: [answerSlugs.parcelNumber, answerSlugs.buildingLawNumber],
  addressSlugs: [answerSlugs.objectStreet, answerSlugs.objectLocation],
  personalDetailsSlugs: [
    answerSlugs.juristicNameApplicant,
    answerSlugs.firstNameApplicant,
    answerSlugs.lastNameApplicant,
  ],
};
