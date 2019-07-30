import { Model, belongsTo } from "ember-cli-mirage";

export default Model.extend({
  instanceState: belongsTo("instance-state")
});
