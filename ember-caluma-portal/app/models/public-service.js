import Model, { attr, belongsTo } from "@ember-data/model";

export default class PublicService extends Model {
  @attr("string") name;
  @belongsTo("public-service-group") serviceGroup;
}
