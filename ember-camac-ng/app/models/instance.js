import Model, { attr, belongsTo, hasMany } from "@ember-data/model";

export default class InstanceModel extends Model {
  @attr("string") identifier;
  @attr("string") name;
  @belongsTo("form") form;
  @hasMany("service") services;
  @hasMany("service") involvedServices;
}
