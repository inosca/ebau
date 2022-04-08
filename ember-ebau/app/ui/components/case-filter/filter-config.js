export default {
  instanceId: {
    type: "input",
  },
  dossierNumber: {
    type: "input",
  },
  applicantName: {
    type: "input",
  },
  street: {
    type: "input",
  },
  municipality: {
    type: "select",
    options: "municipalities",
    valueField: "id",
    labelField: "name",
  },
  parcelNumber: {
    type: "input",
  },
  instanceState: {
    type: "select",
    options: "instanceStates",
    valueField: "id",
    labelField: "uppercaseName",
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
    type: "select",
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
};
