import Model, { attr, belongsTo, hasMany } from "@ember-data/model";

export default class Group extends Model {
  @attr("string") name;

  @belongsTo("role", { inverse: null, async: true }) role;
  @belongsTo("service", { inverse: null, async: true }) service;
  @hasMany("location", { inverse: null, async: true }) locations;
}
