import { helper } from "@ember/component/helper";

import config from "ember-caluma-portal/config/environment";

export default helper(function isApplication([name]) {
  return config.APPLICATION.name === name;
});
