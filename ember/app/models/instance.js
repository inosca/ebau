import Model, { attr, belongsTo, hasMany } from "@ember-data/model";

export default Model.extend({
  identifier: attr("string"),
  creationDate: attr("date"),
  location: belongsTo("location"),
  form: belongsTo("form"),
  fields: hasMany("form-field"),
  attachments: hasMany("attachment"),
  instanceState: belongsTo("instance-state"),
  previousInstanceState: belongsTo("instance-state"),
  group: belongsTo("group"),
});
