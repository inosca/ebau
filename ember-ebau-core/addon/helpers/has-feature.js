import { helper } from "@ember/component/helper";
import { get } from "@ember/object";

import featuresConfig from "ember-ebau-core/config/features";

export function hasFeature(name) {
  const value = get(featuresConfig.features, name) ?? false;

  /* This is needed in order to use env variables in the features definition. As
   * `getOwnConfig().feature` will always return a string and
   * `getOwnConfig().feature === "true"` would be compiled to `false` on build
   * time (when the env variable is not properly set yet), we need to do the
   * string evaluation in runtime.
   *
   * DISCLAIMER: Only ever use macro conditions in features if the feature is
   * enabled/disabled depending on the environment! E.g feature XY is enabled in
   * test and dev but not prod.
   */
  if (typeof value === "string") {
    return ["true", "1"].includes(value.toLowerCase());
  }

  return value;
}

export default helper(([name]) => hasFeature(name));
