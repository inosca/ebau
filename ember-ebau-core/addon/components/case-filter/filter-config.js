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
  keywordSearch: { type: "input" },
  personalDetails: { type: "input" },
  decisionDateAfter: { type: "date", maxDate: "decisionDateBefore" },
  decisionDateBefore: { type: "date", minDate: "decisionDateAfter" },
  inquiryCompletedAfter: { type: "date", maxDate: "inquiryCompletedBefore" },
  inquiryCompletedBefore: { type: "date", minDate: "inquiryCompletedAfter" },
  inquiryCreatedAfter: { type: "date", maxDate: "inquiryCreatedBefore" },
  inquiryCreatedBefore: { type: "date", minDate: "inquiryCreatedAfter" },
  submitDateAfter: { type: "date", maxDate: "submitDateBefore" },
  submitDateBefore: { type: "date", minDate: "submitDateAfter" },
  caseCreatedDateAfter: { type: "date", maxDate: "caseCreatedDateBefore" },
  caseCreatedDateBefore: { type: "date", minDate: "caseCreatedDateAfter" },
  withCantonalParticipation: { type: "toggle-switch" },
  objectionReceived: { type: "toggle-switch" },
  constructionZoneLocation: {
    type: "select",
    options: "constructionZoneLocationOptions",
    valueField: "value",
    labelField: "name",
  },
  municipality: macroCondition(getOwnConfig().application === "ur")
    ? {
        type: "select-multiple",
        options: "municipalities",
        valueField: "id",
        labelField: "name",
      }
    : macroCondition(getOwnConfig().application === "sz")
      ? {
          type: "select",
          options: "municipalities",
          valueField: "id",
          labelField: "name",
        }
      : {
          type: "select",
          options: "municipalitiesFromCaluma",
          valueField: "slug",
          labelField: "label",
          showWithoutOptions: true,
        },
  instanceState: {
    type: "select-multiple",
    options: "instanceStates",
    valueField: "id",
    labelField: macroCondition(getOwnConfig().application === "ur")
      ? "uppercaseName"
      : macroCondition(getOwnConfig().application === "sz")
        ? "description"
        : "name",
    showWithoutOptions: macroCondition(getOwnConfig().application === "sz")
      ? false
      : true,
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
    showWithoutOptions: macroCondition(getOwnConfig().application === "sz")
      ? false
      : true,
  },
  type: {
    type: "select",
    options: "formsSZ",
    valueField: "id",
    labelField: "description",
  },
  form: macroCondition(getOwnConfig().application === "sz")
    ? {
        type: "select",
        options: "formOptions",
        labelField: "name",
      }
    : {
        type: "select",
        options: "forms",
        valueField: "value",
        labelField: "name",
        showWithoutOptions: true,
      },
  responsibleMunicipality: {
    type: "select",
    options: "responsibleMunicipalities",
    valueField: "id",
    labelField: "name",
    showWithoutOptions: true,
  },
  tags: {
    type: "async-select-multiple",
    options: "selectedTags",
    search: "searchTags",
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
  modification: {
    type: "select",
    options: "modificationOptions",
    valueField: "value",
    labelField: "label",
    showWithoutOptions: true,
  },
  legalStateOereb: {
    type: "select-multiple",
    options: "legalStateOerebOptions",
    valueField: "slug",
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
  decision: {
    type: "select-multiple",
    options: "decisionOptions",
    labelField: "label",
    showWithoutOptions: true,
  },
  inquiryAnswer: {
    type: "select-multiple",
    options: "inquiryAnswerOptions",
    labelField: "label",
    showWithoutOptions: true,
  },
};
