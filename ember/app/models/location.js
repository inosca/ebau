import Model, { attr } from "@ember-data/model";
import { hasMany } from "ember-data/relationships";

export default Model.extend({
  name: attr("string"),
  communalFederalNumber: attr("number"),
  groups: hasMany("group")
});
