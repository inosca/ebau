import Model, { belongsTo } from "@ember-data/model";

export default class ResponsibleServiceModel extends Model {
  @belongsTo("instance", { inverse: null, async: true }) instance;
  @belongsTo("user", { inverse: null, async: true }) responsibleUser;
  @belongsTo("service", { inverse: null, async: true }) service;
}
