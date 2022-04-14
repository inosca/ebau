import { macroCondition, getOwnConfig } from "@embroider/macros";

export default {
  address: { type: "input" },
  applicant: { type: "input" },
  builder: { type: "input" },
  dossierNumber: { type: "input" },
  instanceId: { type: "input" },
  instanceIdentifier: { type: "input" },
  intent: { type: "input" },
  landowner: { type: "input" },
  parcel: { type: "input" },
  personalDetails: { type: "input" },
  decisionDateAfter: { type: "date", maxDate: "decisionDateBefore" },
  decisionDateBefore: { type: "date", minDate: "decisionDateAfter" },
  submitDateAfter: { type: "date", maxDate: "submitDateBefore" },
  submitDateBefore: { type: "date", minDate: "submitDateAfter" },
  withCantonalParticipation: { type: "toggle-switch" },

  municipality: macroCondition(getOwnConfig().application === "be")
    ? {
        type: "select",
        options: "municipalitiesFromCaluma",
        valueField: "slug",
        labelField: "label",
        showWithoutOptions: true,
      }
    : macroCondition(getOwnConfig().application === "sz")
    ? {
        type: "select",
        options: "municipalities",
        valueField: "id",
        labelField: "name",
      }
    : {
        type: "select-multiple",
        options: "municipalities",
        valueField: "id",
        labelField: "name",
      },
  instanceState: {
    type: "select-multiple",
    options: "instanceStates",
    valueField: "id",
    labelField: macroCondition(getOwnConfig().application === "be")
      ? "name"
      : macroCondition(getOwnConfig().application === "sz")
      ? "description"
      : "uppercaseName",
    showWithoutOptions: macroCondition(getOwnConfig().application === "be")
      ? true
      : false,
  },
  service: {
    type: "select",
    options: macroCondition(getOwnConfig().application === "sz")
      ? "servicesSZ"
      : "services",
    valueField: "id",
    labelField: "name",
  },
  pendingSanctionsControlInstance: {
    type: "select",
    options: "services",
    valueField: "id",
    labelField: "name",
  },
  buildingPermitType: {
    type: "select-multiple",
    options: "buildingPermitTypes",
  },
  caseStatus: {
    type: "select",
    options: "caseStatusOptions",
    valueField: "status",
    labelField: "label",
  },
  responsibleServiceUser: {
    type: "select",
    options: "responsibleServiceUsers",
    valueField: "id",
    labelField: "fullName",
    showWithoutOptions: macroCondition(getOwnConfig().application === "be")
      ? true
      : false,
  },
  type: {
    type: "select",
    options: "formsSZ",
    valueField: "id",
    labelField: "description",
  },
  form: macroCondition(getOwnConfig().application === "be")
    ? {
        type: "select",
        options: "forms",
        valueField: "value",
        labelField: "name",
        showWithoutOptions: true,
      }
    : {
        type: "select",
        options: "formOptions",
        labelField: "name",
      },
  responsibleMunicipality: {
    type: "select",
    options: "responsibleMunicipalities",
    valueField: "id",
    labelField: "name",
    showWithoutOptions: true,
  },
  tags: {
    type: "select-multiple",
    options: "tags",
    valueField: "name",
    labelField: "name",
    showWithoutOptions: true,
  },
  paper: {
    type: "select",
    options: "paperOptions",
    valueField: "value",
    labelField: "label",
    showWithoutOptions: true,
  },
  inquiryState: {
    type: "select",
    options: "inquiryStateOptions",
    valueField: "value",
    labelField: "label",
    showWithoutOptions: true,
  },
};
