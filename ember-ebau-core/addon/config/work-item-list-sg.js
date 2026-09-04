export default {
  availableTasks: {},
  columns(status, role) {
    return [
      "task",
      "instance",
      role === "service" ? "municipality" : null,
      "description",
      ...(status === "COMPLETED"
        ? ["closedAt", "closedBy"]
        : ["deadline", "responsible"]),
    ].filter((value) => value !== null);
  },
};
