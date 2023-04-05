import Model, { attr, belongsTo } from "@ember-data/model";

export default class CommunicationTopicModel extends Model {
  @attr subject;
  @attr hasUnread;
  @attr dossierNumber;
  @attr("date") created;
  @attr involvedEntities;
  @attr allowReplies;

  @belongsTo instance;
  @belongsTo("user") initiatedBy;
}
