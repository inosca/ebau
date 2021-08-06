import Model, { attr, belongsTo } from "@ember-data/model";

export default class JournalEntryModel extends Model {
  @attr("string") text;
  @attr("date") creationDate;
  @attr("string") visibility;

  @belongsTo instance;
  @belongsTo user;
  @belongsTo service;

  get visibilityBoolean() {
    switch (this.visibility) {
      case "authorities":
        return true;
      case "own_organization":
        return false;
      default:
        return false;
    }
  }
}
