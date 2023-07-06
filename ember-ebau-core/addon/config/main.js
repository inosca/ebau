import { importSync, getOwnConfig, macroCondition } from "@embroider/macros";

let config;
if (macroCondition(getOwnConfig().application === "be")) {
  config = importSync("ember-ebau-core/config/main-be");
} else if (macroCondition(getOwnConfig().application === "ur")) {
  config = importSync("ember-ebau-core/config/main-ur");
} else if (macroCondition(getOwnConfig().application === "sz")) {
  config = importSync("ember-ebau-core/config/main-sz");
} else if (macroCondition(getOwnConfig().application === "gr")) {
  config = importSync("ember-ebau-core/config/main-gr");
} else if (macroCondition(getOwnConfig().application === "so")) {
  config = importSync("ember-ebau-core/config/main-so");
} else if (macroCondition(getOwnConfig().application === "demo")) {
  config = importSync("ember-ebau-core/config/main-demo");
}

const sharedConfig = {
  maxDossierImportSize: 1500000000, // 1.5GB
};

export default { ...sharedConfig, ...config.default };
