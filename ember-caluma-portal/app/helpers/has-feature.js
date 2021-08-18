import { helper } from "@ember/component/helper";
import { get } from "@ember/object";

import config from "caluma-portal/config/environment";

export function hasFeature(featureName) {
  return Boolean(get(config, `APPLICATION.features.${featureName}`));
}

export default helper(([featureName]) => hasFeature(featureName));
