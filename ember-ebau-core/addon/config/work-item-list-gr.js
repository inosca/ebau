export default {
  showTaskFilter: true,
  availableTasks: {
    roles: {
      municipality: [
        "formal-exam",
        "publication",
        "init-distribution",
        "check-inquiries",
        "decision",
        "construction-acceptance",
      ],
    },
    services: {
      1: ["inquiry", "check-inquiries", "check-additional-demand"],
    },
    default: [],
  },
  columns(status, role) {
    return [
      "task",
      "instance",
      role === "municipality" ? "applicants" : null,
      ...(role === "service" ? ["municipality", "applicants"] : []),
      "description",
      ...(status === "COMPLETED"
        ? ["closedAt", "closedBy"]
        : ["deadline", "responsible"]),
    ].filter((value) => value !== null);
  },
};
