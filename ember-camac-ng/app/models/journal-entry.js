import Model, { attr, belongsTo } from "@ember-data/model";

export default class HistoryEntryModel extends Model {
  @attr("string") text;
  @attr("date") creationDate;

  @belongsTo instance;
  @belongsTo user;
  @belongsTo service;
}
