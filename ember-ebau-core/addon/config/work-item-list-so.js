import { sharedConfig } from "./work-item-list";

export default {
  showFilterPresets: true,
  availableTasks: {},
  columns(status, role) {
    return [
      ...sharedConfig.columns(status),
      ...(role !== "municipality" ? ["municipality"] : []),
    ];
  },
};
