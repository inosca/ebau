import { macroCondition, getOwnConfig } from "@embroider/macros";

let config;
if (macroCondition(getOwnConfig().canton === "ur")) {
  config = {
    columns: {
      caluma: {
        municipality: [
          "instanceId",
          "dossierNr",
          "form",
          "municipality",
          "user",
          "applicant",
          "intent",
          "street",
          "instanceState",
        ],
        coordination: [
          "instanceId",
          "dossierNr",
          "coordination",
          "form",
          "municipality",
          "user",
          "applicant",
          "intent",
          "street",
          "instanceState",
        ],
        service: [
          "deadlineColor",
          "instanceId",
          "dossierNr",
          "coordination",
          "form",
          "municipality",
          "applicant",
          "intent",
          "street",
          "processingDeadline",
        ],
        default: [
          "dossierNr",
          "municipality",
          "applicant",
          "intent",
          "street",
          "parcelNumbers",
        ],
      },
    },
  };
}
if (macroCondition(getOwnConfig().canton === "be")) {
  config = {};
}
if (macroCondition(getOwnConfig().canton === "sz")) {
  config = {
    columns: {
      caluma: ["dossierNr", "caseDocumentFormName", "intent", "caseStatus"],
      "camac-ng": [
        "dossierNr",
        "instanceFormDescription",
        "locationSZ",
        "builderSZ",
        "intentSZ",
        "instanceStateDescription",
      ],
    },
  };
}
export default config;
