import Model, { belongsTo } from "@ember-data/model";

export default class ResponsibleServiceModel extends Model {
  @belongsTo instance;
  @belongsTo("user") responsibleUser;
  @belongsTo service;
}
