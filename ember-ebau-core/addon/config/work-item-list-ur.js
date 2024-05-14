export default {
  showTaskFilter: true,
  availableTasks: {
    roles: {
      municipality: [
        "complete-check",
        "init-distribution",
        "check-inquiries",
        "decision",
        "init-construction-monitoring",
        "complete-instance",
      ],
      service: ["inquiry", "check-inquiries"],
      coordination: ["inquiry", "check-inquiries"],
    },
    services: {},
    default: [],
  },
};
