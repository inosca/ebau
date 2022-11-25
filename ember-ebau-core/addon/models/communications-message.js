import Model, { attr, belongsTo, hasMany } from "@ember-data/model";

export default class CommunicationMessageModel extends Model {
  @attr body;
  @attr createdAt;
  @attr isRead;

  @belongsTo communicationsTopic;
  @belongsTo("communications-entity") createdBy;
  @hasMany("communications-entity") readBy;
}
