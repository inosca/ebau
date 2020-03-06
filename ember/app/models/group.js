import Model, { attr, belongsTo, hasMany } from "@ember-data/model";

export default Model.extend({
  name: attr("string"),
  role: belongsTo("role"),
  locations: hasMany("location")
});
