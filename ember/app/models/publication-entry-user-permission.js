import Model, { attr, belongsTo } from "@ember-data/model";

export default Model.extend({
  status: attr("string"),
  publicationEntry: belongsTo("publication-entry")
});
