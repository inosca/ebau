import Model, { attr, belongsTo, hasMany } from "@ember-data/model";

export default class CommunicationMessageModel extends Model {
  @attr body;
  @attr createdAt;
  @attr isRead;

  @belongsTo("communications-topic") topic;
  @belongsTo("communications-entity") createdBy;
  @belongsTo("user") createdBy;
  @hasMany("communications-entity") readBy;
}
