import { Model, belongsTo } from "miragejs";

export default Model.extend({
  user: belongsTo("user"),
  invitee: belongsTo("user"),
  instance: belongsTo("instance"),
});
