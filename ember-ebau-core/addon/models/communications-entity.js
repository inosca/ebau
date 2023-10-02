import Model, { attr, belongsTo } from "@ember-data/model";

export default class CommunicationEntityModel extends Model {
  @attr isApplicant;
  @belongsTo("service", { inverse: null, async: true }) service;
}
