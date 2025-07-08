export default {
  showTaskFilter: true,
  showFilterPresets: true,
  taskFilterAsDropdown: true,
  completeAction: true,
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
        "check-distribution",
        "init-construction-monitoring",
      ],
      service: ["inquiry", "check-inquiries"],
      subservice: ["inquiry"],
    },
    serviceGroups: {
      "service-afb": ["check-pa", "cantonal-exam", "check-document-supplement"],
    },
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
