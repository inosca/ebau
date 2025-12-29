import { sharedConfig } from "./work-item-list";

export default {
  showTaskFilter: true,
  showFilterPresets: true,
  taskFilterAsDropdown: true,
  availableTasks: {},
  columns(status, role) {
    return [
      ...sharedConfig.columns(status),
      ...(role !== "municipality" ? ["municipality"] : []),
    ];
  },
};
