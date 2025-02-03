export default {
  showTaskFilter: true,
  availableTasks: {
    roles: {
      "authority-bab": [
        "inquiry",
        "check-inquiries",
        "check-additional-demand",
      ],
      municipality: [
        "formal-exam",
        "publication",
        "init-distribution",
        "check-inquiries",
        "decision",
        "construction-acceptance",
      ],
      service: ["inquiry", "check-inquiries"],
      subservice: ["inquiry"],
      uso: ["inquiry"],
    },
    services: [],
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
