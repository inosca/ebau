import Model, { attr, belongsTo, hasMany } from "@ember-data/model";

export default class CommunicationTopicModel extends Model {
  @attr subject;
  @attr created;

  @belongsTo("instance") instance;
  @belongsTo("user") initiatedBy;
  @hasMany("communications-entity") involvedEntities;
}
