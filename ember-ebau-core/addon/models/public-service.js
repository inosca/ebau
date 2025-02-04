import Model, { attr, belongsTo } from "@ember-data/model";

export default class PublicService extends Model {
  @attr name;
  @attr website;
  @attr logo;
  @belongsTo("public-service-group", { inverse: null, async: true })
  serviceGroup;
  @belongsTo("public-service", { inverse: null, async: true }) serviceParent;
}
