export default {
  name: "so",
  languages: ["de"],
  fallbackLanguage: "de",
  allowApplicantManualWorkItem: false,
  instanceStates: {
    new: 1,
  },
  answerSlugs: {},
  personalSuggestions: {
    tableQuestions: [],
    firstNameRegexp: "^todo-.*$",
    lastNameRegexp: "^todo-.*$",
    juristicNameRegexp: "^todo.*$",
    emailRegexp: "^e-mail-.*$",
  },
  intentSlugs: [],
  paperInstances: {
    allowedGroups: {
      roles: [],
      serviceGroups: [],
    },
  },
};
