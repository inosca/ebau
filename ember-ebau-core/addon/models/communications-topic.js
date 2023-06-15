import Model, { attr, belongsTo } from "@ember-data/model";

export default class CommunicationTopicModel extends Model {
  @attr subject;
  @attr hasUnread;
  @attr dossierNumber;
  @attr("date") created;
  @attr({ defaultValue: true }) allowReplies;
  @attr initiatedByEntity;
  @attr involvedEntities;

  @belongsTo instance;
  @belongsTo("user") initiatedBy;
}
