import Model, { attr, belongsTo, hasMany } from "@ember-data/model";

export default class ServiceContentModel extends Model {
  @attr content;

  @belongsTo("service", { inverse: null, async: false }) service;
  @hasMany("forms", { inverse: null, async: false }) forms;
}
