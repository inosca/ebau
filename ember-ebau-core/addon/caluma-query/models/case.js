import { macroCondition, getOwnConfig } from "@embroider/macros";

import be from "ember-ebau-core/caluma-query/models/case-be";
import gr from "ember-ebau-core/caluma-query/models/case-gr";
import sz from "ember-ebau-core/caluma-query/models/case-sz";
import ur from "ember-ebau-core/caluma-query/models/case-ur";

let config;
if (macroCondition(getOwnConfig().application === "be")) {
  config = be;
} else if (macroCondition(getOwnConfig().application === "ur")) {
  config = ur;
} else if (macroCondition(getOwnConfig().application === "sz")) {
  config = sz;
} else if (macroCondition(getOwnConfig().application === "gr")) {
  config = gr;
}
export default config;
