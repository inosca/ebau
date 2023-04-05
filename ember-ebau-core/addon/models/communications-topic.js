import Model, { attr, belongsTo } from "@ember-data/model";

export default class CommunicationTopicModel extends Model {
  @attr subject;
  @attr hasUnread;
  @attr dossierNumber;
  @attr("date") created;
  @attr involvedEntities;
  @attr({ defaultValue: true }) allowReplies;

  @belongsTo instance;
  @belongsTo("user") initiatedBy;
}
