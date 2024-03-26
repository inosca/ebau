import { importSync, getOwnConfig, macroCondition } from "@embroider/macros";

let config;
if (macroCondition(getOwnConfig().application === "demo")) {
  config = importSync("ember-ebau-core/config/attachments-demo");
} else if (macroCondition(getOwnConfig().application === "be")) {
  config = importSync("ember-ebau-core/config/attachments-be");
} else if (macroCondition(getOwnConfig().application === "ur")) {
  config = importSync("ember-ebau-core/config/attachments-ur");
} else if (macroCondition(getOwnConfig().application === "gr")) {
  config = importSync("ember-ebau-core/config/attachments-gr");
} else if (macroCondition(getOwnConfig().application === "so")) {
  config = importSync("ember-ebau-core/config/attachments-so");
}
export default config.default;
