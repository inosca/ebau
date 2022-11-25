import Model, { attr, belongsTo, hasMany } from "@ember-data/model";

export default class CommunicationTopicModel extends Model {
  @attr subject;
  @attr hasUnread;
  @attr("date") created;

  @belongsTo instance;
  @belongsTo("user") initiatedBy;
  @hasMany("communications-entity") involvedEntities;
}
