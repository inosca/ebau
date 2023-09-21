import Model, { attr, belongsTo } from "@ember-data/model";

export default class UserGroupModel extends Model {
  @attr email; // write only
  @attr createdAt;

  @belongsTo("user", { inverse: null, async: false }) user;
  @belongsTo("group", { inverse: null, async: false }) group;
  @belongsTo("user", { inverse: null, async: false }) createdBy;
}
