import { helper } from "@ember/component/helper";
import { get } from "@ember/object";

import mainConfig from "ember-ebau-core/config/main";

export default helper(function getMainConfig([key]) {
  return get(mainConfig, key);
});
