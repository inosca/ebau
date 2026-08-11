import { helper } from "@ember/component/helper";

import mainConfig from "ember-ebau-core/config/main";

export function isApplication(...names) {
  return names.includes(mainConfig.name);
}

export default helper((names) => isApplication(...names));
