import Model, { attr, belongsTo } from "@ember-data/model";

export default class InstancePermissionModel extends Model {
  @attr permissions;

  @belongsTo("instance", { async: true, inverse: null }) instance;
}
