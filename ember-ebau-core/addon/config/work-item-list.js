import { importSync, getOwnConfig, macroCondition } from "@embroider/macros";

let config;
if (macroCondition(getOwnConfig().application === "be")) {
  config = importSync("ember-ebau-core/config/work-item-list-be");
} else if (macroCondition(getOwnConfig().application === "ur")) {
  config = importSync("ember-ebau-core/config/work-item-list-ur");
} else if (macroCondition(getOwnConfig().application === "sz")) {
  config = importSync("ember-ebau-core/config/work-item-list-sz");
} else if (macroCondition(getOwnConfig().application === "gr")) {
  config = importSync("ember-ebau-core/config/work-item-list-gr");
} else if (macroCondition(getOwnConfig().application === "so")) {
  config = importSync("ember-ebau-core/config/work-item-list-so");
} else if (macroCondition(getOwnConfig().application === "test")) {
  config = importSync("ember-ebau-core/config/work-item-list-test");
}

export default config.default;
