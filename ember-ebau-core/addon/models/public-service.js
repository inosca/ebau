import Model, { attr, belongsTo } from "@ember-data/model";

export default class PublicService extends Model {
  @attr name;
  @attr website;
  @belongsTo("public-service-group") serviceGroup;
}
