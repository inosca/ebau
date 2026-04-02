import { importSync, getOwnConfig, macroCondition } from "@embroider/macros";

let config;
if (macroCondition(getOwnConfig().application === "be")) {
  config = importSync("ember-ebau-core/config/statistics-export-be");
} else if (macroCondition(getOwnConfig().application === "ag")) {
  config = importSync("ember-ebau-core/config/statistics-export-ag");
} else if (macroCondition(getOwnConfig().application === "test")) {
  config = importSync("ember-ebau-core/config/statistics-export-test");
} else {
  // Fallback if no application matches
  config = { default: { exportTypes: {} } };
}
export default config.default;
