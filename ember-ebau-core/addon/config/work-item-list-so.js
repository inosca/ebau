import { sharedConfig } from "./work-item-list";

export default {
  showTaskFilter: false,
  columns(status, role) {
    return [
      ...sharedConfig.columns(status),
      ...(role !== "municipality" ? ["municipality"] : []),
    ];
  },
};
