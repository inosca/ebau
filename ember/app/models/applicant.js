import Model, { attr, belongsTo } from "@ember-data/model";

export default Model.extend({
  email: attr("string"),
  instance: belongsTo("instance"),
});
