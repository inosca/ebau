import { getOwnConfig, macroCondition } from "@embroider/macros";

import be from "ember-ebau-core/config/main-be";
import gr from "ember-ebau-core/config/main-gr";
// import sz from "ember-ebau-core/config/main-sz";
// import ur from "ember-ebau-core/config/main-ur";

let config;
if (macroCondition(getOwnConfig().application === "be")) {
  config = be;
  // } else if (macroCondition(getOwnConfig().application === "ur")) {
  //   config = ur;
  // } else if (macroCondition(getOwnConfig().application === "sz")) {
  //   config = sz;
} else if (macroCondition(getOwnConfig().application === "gr")) {
  config = gr;
}
export default config;
