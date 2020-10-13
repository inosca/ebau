import Model, { attr, belongsTo, hasMany } from "@ember-data/model";

export default class InstanceModel extends Model {
  @attr identifier;
  @attr name;
  @belongsTo form;
  @belongsTo instanceState;
  @belongsTo user;
  @hasMany services;
  @hasMany("service") involvedServices;
}
