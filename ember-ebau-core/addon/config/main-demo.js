export default {
  instanceStates: {
    new: 1,
    subm: 120004,
    circ: 120005,
    finished: 120006,
  },
  answerSlugs: {},
  personalSuggestions: {
    tableQuestions: [
      "personalien-gesuchstellerin",
      "personalien-vertreterin-mit-vollmacht",
      "personalien-grundeigentumerin",
      "personalien-projektverfasserin",
      "personalien-gebaudeeigentumerin",
      "personalien-sb",
    ],
    firstNameRegexp: "^vorname-.*$",
    lastNameRegexp: "^name-.*$",
    juristicNameRegexp: "^name-juristische-person.*$",
    emailRegexp: "^e-mail-.*$",
  },
  communication: {
    rolesWithApplicantContact: ["activeOrInolvedLeadAuthority"],
  },
  modification: {
    allowForms: ["baugesuch"],
    disallowStates: ["new", "finished"],
  },
};
