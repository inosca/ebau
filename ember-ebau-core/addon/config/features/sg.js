import { getOwnConfig, isDevelopingApp } from "@embroider/macros";

export default {
  watermark: isDevelopingApp() || getOwnConfig().enableWatermark,
};
