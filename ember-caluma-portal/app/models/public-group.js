import Model, { attr, belongsTo } from "@ember-data/model";

export default class PublicGroup extends Model {
  @attr("string") name;
  @belongsTo("public-role") role;
  @belongsTo("public-service") service;
}
