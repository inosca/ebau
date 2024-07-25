import { importSync, getOwnConfig, macroCondition } from "@embroider/macros";

let config;
if (macroCondition(getOwnConfig().application === "ur")) {
  config = importSync("ember-ebau-core/config/additional-demands-ur");
}
export default config?.default ?? {};
