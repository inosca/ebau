import Model, { attr, belongsTo, hasMany } from "@ember-data/model";

export default class Group extends Model {
  @attr("string") name;

  @belongsTo("role") role;
  @belongsTo("service") service;
  @hasMany("location") locations;
}
