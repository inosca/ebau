import Model from "ember-data/model";
import attr from "ember-data/attr";
import { belongsTo } from "ember-data/relationships";

export default Model.extend({
  publication_date: attr("date"),
  is_published: attr("boolean"),
  description: attr("string"),
  instance: belongsTo("instance")
});
