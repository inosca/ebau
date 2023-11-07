import { importSync, getOwnConfig, macroCondition } from "@embroider/macros";

let features;
if (macroCondition(getOwnConfig().application === "be")) {
  features = importSync("ember-ebau-core/config/features/be");
} else if (macroCondition(getOwnConfig().application === "ur")) {
  features = importSync("ember-ebau-core/config/features/ur");
} else if (macroCondition(getOwnConfig().application === "sz")) {
  features = importSync("ember-ebau-core/config/features/sz");
} else if (macroCondition(getOwnConfig().application === "gr")) {
  features = importSync("ember-ebau-core/config/features/gr");
} else if (macroCondition(getOwnConfig().application === "so")) {
  features = importSync("ember-ebau-core/config/features/so");
} else if (macroCondition(getOwnConfig().application === "demo")) {
  features = importSync("ember-ebau-core/config/features/demo");
}

export default { features: features?.default ?? {} };
