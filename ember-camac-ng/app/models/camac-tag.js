import Model, { attr, belongsTo } from "@ember-data/model";

export default class CamacTagModel extends Model {
  @attr name;
  @belongsTo("service", { inverse: null, async: true }) service;
  @belongsTo("instance", { inverse: null, async: true }) instance;
}
