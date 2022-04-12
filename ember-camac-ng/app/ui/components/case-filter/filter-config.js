export default {
  instanceId: {
    type: "input",
  },
  dossierNumber: {
    type: "input",
  },
  dossierNumberSZ: {
    type: "input",
  },
  instanceIdentifier: {
    type: "input",
  },
  applicantName: {
    type: "input",
  },
  street: {
    type: "input",
  },
  municipality: {
    type: "select-multiple",
    options: "municipalities",
    valueField: "id",
    labelField: "name",
  },
  locationSZ: {
    type: "select",
    options: "municipalities",
    valueField: "id",
    labelField: "name",
  },
  parcelNumber: {
    type: "input",
  },
  instanceState: {
    type: "select-multiple",
    options: "instanceStates",
    valueField: "id",
    labelField: "uppercaseName",
  },
  instanceStateDescription: {
    type: "select-multiple",
    options: "instanceStates",
    valueField: "id",
    labelField: "description",
  },
  service: {
    type: "select",
    options: "services",
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
  createdAfter: {
    type: "date",
    maxDate: "createdBefore",
  },
  createdBefore: {
    type: "date",
    minDate: "createdAfter",
  },
  intent: {
    type: "input",
  },
  caseStatus: {
    type: "select",
    options: "caseStatusOptions",
    optionValues: ["RUNNING", "COMPLETED"],
    valueField: "status",
    labelField: "label",
  },
  caseDocumentFormName: {
    type: "select",
    options: "formOptions",
    labelField: "name",
  },
  responsibleServiceUser: {
    type: "select",
    options: "responsibleServiceUsers",
    valueField: "value",
  },
  addressSZ: {
    type: "input",
  },
  intentSZ: {
    type: "input",
  },
  plotSZ: {
    type: "input",
  },
  builderSZ: {
    type: "input",
  },
  landownerSZ: {
    type: "input",
  },
  applicantSZ: {
    type: "input",
  },
  submitDateAfterSZ: {
    type: "date",
    maxDate: "submitDateBeforeSZ",
  },
  submitDateBeforeSZ: {
    type: "date",
    minDate: "submitDateAfterSZ",
  },
  serviceSZ: {
    type: "select",
    options: "servicesSZ",
    valueField: "id",
    labelField: "name",
  },
  formSZ: {
    type: "select",
    options: "formsSZ",
    valueField: "id",
    labelField: "description",
  },
};
