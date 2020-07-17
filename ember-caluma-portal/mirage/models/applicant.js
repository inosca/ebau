import { Model, belongsTo } from "ember-cli-mirage";

export default Model.extend({
  user: belongsTo("user"),
  invitee: belongsTo("user"),
  instance: belongsTo("instance"),
});
