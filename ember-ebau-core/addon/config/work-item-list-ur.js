export default {
  pageSize: 50,
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
      service: ["inquiry"],
      coordination: ["inquiry", "check-inquiries"],
    },
    services: {},
    default: [],
  },
  columns(status) {
    return [
      "task",
      "instance",
      "description",
      "municipality",
      "applicants",
      ...(status === "COMPLETED"
        ? ["closedAt", "closedBy"]
        : ["deadline", "responsible"]),
    ].filter((value) => value !== null);
  },
};
