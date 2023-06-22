import { importSync, getOwnConfig, macroCondition } from "@embroider/macros";

let config;
if (macroCondition(getOwnConfig().application === "be")) {
  config = importSync("ember-ebau-core/config/case-table-be");
} else if (macroCondition(getOwnConfig().application === "ur")) {
  config = importSync("ember-ebau-core/config/case-table-ur");
} else if (macroCondition(getOwnConfig().application === "sz")) {
  config = importSync("ember-ebau-core/config/case-table-sz");
} else if (macroCondition(getOwnConfig().application === "gr")) {
  config = importSync("ember-ebau-core/config/case-table-gr");
}
export default config.default;
