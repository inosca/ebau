import Model, { attr, belongsTo } from "@ember-data/model";

export default Model.extend({
  publication_date: attr("date"),
  is_published: attr("boolean"),
  description: attr("string"),
  instance: belongsTo("instance")
});
