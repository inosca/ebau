import Model, { attr, hasMany } from "@ember-data/model";

export default Model.extend({
  name: attr("string"),
  communalFederalNumber: attr("number"),
  groups: hasMany("group")
});
