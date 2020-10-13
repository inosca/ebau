import Model, { attr, belongsTo } from "@ember-data/model";

export default class JournalEntryModel extends Model {
  @attr("string") text;
  @attr("date") creationDate;
  @attr("string") visibility;

  @belongsTo instance;
  @belongsTo user;
  @belongsTo service;
}
