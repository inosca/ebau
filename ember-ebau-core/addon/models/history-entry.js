import Model, { attr, belongsTo } from "@ember-data/model";

export default class HistoryEntryModel extends Model {
  @attr("string") title;
  @attr("string") body;
  @attr("date") createdAt;
  @attr("string") historyType;

  @belongsTo("instance", { inverse: null, async: true }) instance;
  @belongsTo("user", { inverse: null, async: true }) user;
  @belongsTo("service", { inverse: null, async: true }) service;

  get icon() {
    switch (this.historyType) {
      case "notification":
        return "envelope";
      case "status-change":
        return "circle-check";
      default:
        return null;
    }
  }
}
