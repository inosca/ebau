import Model, { attr, hasMany, belongsTo } from "@ember-data/model";

export default class ServiceModel extends Model {
  @attr("string") name;
  @attr("string") description;
  @attr("string") phone;
  @attr("string") zip;
  @attr("string") city;
  @attr("string") address;
  @attr("string") email;
  @attr("string") website;
  @attr("number") notification;
  @attr("number") responsibilityConstructionControl;
  @hasMany("user", { inverse: "service", async: true }) users;
  @hasMany("activation", { inverse: "service", async: true }) activations;
  @belongsTo("public-service-group", { inverse: null, async: true })
  serviceGroup;
  @belongsTo("service", { inverse: null, async: true }) serviceParent;
}
