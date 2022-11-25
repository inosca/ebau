import Model, { attr, belongsTo } from "@ember-data/model";

export default class CommunicationEntityModel extends Model {
  @attr isApplicant;
  @belongsTo("service") service;
}
