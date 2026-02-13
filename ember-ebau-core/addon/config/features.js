import { importSync, getOwnConfig, macroCondition } from "@embroider/macros";

function validateFeatureConfig(obj, prefix = null) {
  for (const [k, v] of Object.entries(obj)) {
    const type = typeof v;
    const fullKey = prefix ? [prefix, k].join(".") : k;

    if (type === "object") {
      validateFeatureConfig(v, fullKey);
    } else if (type !== "boolean") {
      if (
        type === "string" &&
        ["1", "0", "true", "false"].includes(v.toLowerCase())
      ) {
        // `getOwnConfig` will always return a string. For more information,
        // check the comment in the helper:
        // `ember-ebau-core/addon/helpers/has-feature.js`.
        continue;
      }

      throw new Error(
        `Unexpected type "${type}" for feature flag "${fullKey}". Only boolean values or nested objects are allowed.`,
      );
    }
  }
}

let features = {};
if (macroCondition(getOwnConfig().application === "be")) {
  features = importSync("ember-ebau-core/config/features/be").default;
} else if (macroCondition(getOwnConfig().application === "ur")) {
  features = importSync("ember-ebau-core/config/features/ur").default;
} else if (macroCondition(getOwnConfig().application === "sz")) {
  features = importSync("ember-ebau-core/config/features/sz").default;
} else if (macroCondition(getOwnConfig().application === "gr")) {
  features = importSync("ember-ebau-core/config/features/gr").default;
} else if (macroCondition(getOwnConfig().application === "so")) {
  features = importSync("ember-ebau-core/config/features/so").default;
} else if (macroCondition(getOwnConfig().application === "ag")) {
  features = importSync("ember-ebau-core/config/features/ag").default;
} else if (macroCondition(getOwnConfig().application === "sg")) {
  features = importSync("ember-ebau-core/config/features/sg").default;
} else if (macroCondition(getOwnConfig().application === "demo")) {
  features = importSync("ember-ebau-core/config/features/demo").default;
}

validateFeatureConfig(features);

export default { features };
