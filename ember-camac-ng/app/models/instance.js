import Model, { attr, belongsTo, hasMany } from "@ember-data/model";

export default class InstanceModel extends Model {
  @attr("string") identifier;
  @belongsTo("form") form;
  @hasMany("service") services;
}
