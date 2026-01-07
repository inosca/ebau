export default {
  pageSize: 50,
  showTaskFilter: true,
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
