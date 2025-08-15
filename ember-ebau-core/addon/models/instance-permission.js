import Model, { attr, belongsTo } from "@ember-data/model";

export default class InstancePermissionModel extends Model {
  @attr permissions;
  @attr currentAccessLevels;

  @belongsTo("instance", { async: true, inverse: null }) instance;
}
