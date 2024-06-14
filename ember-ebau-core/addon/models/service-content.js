import Model, { attr, belongsTo } from "@ember-data/model";

export default class ServiceContentModel extends Model {
  @attr id;
  @attr content;

  @belongsTo("service", { inverse: null, async: false }) service;
}
