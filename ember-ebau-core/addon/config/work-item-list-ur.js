export default {
  pageSize: 50,
  availableTasks: {},
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
