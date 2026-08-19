import { importSync, getOwnConfig, macroCondition } from "@embroider/macros";

// Cantons using alexandria don't need a specific configuration, the allowed
// mime types are configured on the alexandria categories.
const defaultConfig = {
  allowedMimetypes: ["application/pdf", "image/png", "image/jpeg"],
  useConfidential: false,
};

let config;
if (macroCondition(getOwnConfig().application === "demo")) {
  config = importSync("ember-ebau-core/config/attachments-demo");
} else if (macroCondition(getOwnConfig().application === "be")) {
  config = importSync("ember-ebau-core/config/attachments-be");
} else if (macroCondition(getOwnConfig().application === "ur")) {
  config = importSync("ember-ebau-core/config/attachments-ur");
}

export default { ...defaultConfig, ...config?.default };
