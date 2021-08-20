import Model, { attr, belongsTo } from "@ember-data/model";

export default class JournalEntryModel extends Model {
  @attr("string") text;
  @attr("date") creationDate;
  @attr("journalVisibility") visibility;
  @attr("boolean") edit;

  @belongsTo instance;
  @belongsTo user;
  @belongsTo service;
}
