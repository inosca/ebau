import Model, { attr, belongsTo } from "@ember-data/model";

export default class HistoryEntryModel extends Model {
  @attr("string") title;
  @attr("string") body;
  @attr("date") createdAt;
  @attr("string") historyType;

  @belongsTo instance;
  @belongsTo user;
  @belongsTo service;

  get icon() {
    switch (this.historyType) {
      case "notification":
        return "envelope";
      case "status-change":
        return "check-circle";
      default:
        return null;
    }
  }
}
