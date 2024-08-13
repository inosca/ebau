import Model, { attr, belongsTo } from "@ember-data/model";

export default class JournalEntryModel extends Model {
  @attr("string") text;
  @attr("date") creationDate;
  @attr("journalVisibility") visibility;
  @attr("boolean") edit;
  @attr("string") duration;

  @belongsTo("instance", { inverse: null, async: true }) instance;
  @belongsTo("public-user", { inverse: null, async: true }) user;
  @belongsTo("public-service", { inverse: null, async: true }) service;
}
