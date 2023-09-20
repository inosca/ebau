import Model, { attr, belongsTo } from "@ember-data/model";

export default class UserGroupModel extends Model {
  @attr email; // write only
  @attr createdAt;

  @belongsTo("user", { invers: null, async: false }) user;
  @belongsTo("group", { invers: null, async: false }) group;
  @belongsTo("user", { invers: null, async: false }) createdBy;
}
