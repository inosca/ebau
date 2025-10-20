import Model, { attr, belongsTo } from "@ember-data/model";

export default class UserGroupInvitationModel extends Model {
  @attr email;
  @attr createdAt;
  @attr expiresAt;
  @belongsTo("group", { inverse: null, async: false }) group;
  @belongsTo("user", { inverse: null, async: false }) createdBy;
}
