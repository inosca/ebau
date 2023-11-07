import { helper } from "@ember/component/helper";
import { get } from "@ember/object";

import featuresConfig from "ember-ebau-core/config/features";

export function hasFeature(name) {
  return get(featuresConfig.features, name) ?? false;
}

export default helper(([name]) => hasFeature(name));
