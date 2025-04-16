export default {
  showTaskFilter: true,
  taskFilterAsDropdown: true,
  availableTasks: {
    includeTemplates: true,
    roles: {
      municipality: [
        "formal-exam",
        "publication",
        "information-of-neighbors",
        "init-distribution",
        "check-inquiries",
        "decision",
      ],
      service: ["inquiry", "check-inquiries"],
      subservice: ["inquiry"],
    },
    services: {},
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
