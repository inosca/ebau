import { Model, belongsTo, attr } from "ember-cli-mirage";

export default Model.extend({
  createdAt: attr,
  status: attr,

  user: belongsTo(),
});
