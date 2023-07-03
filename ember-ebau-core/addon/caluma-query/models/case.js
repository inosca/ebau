import { importSync, macroCondition, getOwnConfig } from "@embroider/macros";

let config;
if (macroCondition(getOwnConfig().application === "be")) {
  config = importSync("ember-ebau-core/caluma-query/models/case-be");
} else if (macroCondition(getOwnConfig().application === "ur")) {
  config = importSync("ember-ebau-core/caluma-query/models/case-ur");
} else if (macroCondition(getOwnConfig().application === "sz")) {
  config = importSync("ember-ebau-core/caluma-query/models/case-sz");
} else if (macroCondition(getOwnConfig().application === "gr")) {
  config = importSync("ember-ebau-core/caluma-query/models/case-gr");
} else if (macroCondition(getOwnConfig().application === "so")) {
  config = importSync("ember-ebau-core/caluma-query/models/case-so");
}

export default config.default;
