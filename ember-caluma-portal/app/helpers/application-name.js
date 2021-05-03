import { helper } from "@ember/component/helper";

import config from "caluma-portal/config/environment";

export default helper(function () {
  return config.APPLICATION.name;
});
