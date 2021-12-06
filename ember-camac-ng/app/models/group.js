import Model, { attr, belongsTo, hasMany } from "@ember-data/model";

export default class Group extends Model {
  @attr("string") name;

  @belongsTo("role") role;
  @hasMany("location") locations;
}
