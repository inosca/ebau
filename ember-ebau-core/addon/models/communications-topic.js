import Model, { attr, belongsTo, hasMany } from "@ember-data/model";

export default class CommunicationTopicModel extends Model {
  @attr subject;
  @attr hasUnread;
  @attr dossierNumber;
  @attr("date") created;
  @attr({ defaultValue: true }) allowReplies;
  @attr initiatedByEntity;
  @attr involvedEntities;

  @belongsTo("instance", { inverse: null, async: true }) instance;
  @belongsTo("user", { inverse: null, async: true }) initiatedBy;
  @hasMany("user", { inverse: null, async: true }) responsibleServiceUsers;
}
