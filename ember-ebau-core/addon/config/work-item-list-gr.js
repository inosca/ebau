export default {
  showTaskFilter: false,
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
