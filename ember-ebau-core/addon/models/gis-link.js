import Model, { attr, hasMany, belongsTo } from "@ember-data/model";

export default class GisLinkModel extends Model {
  @attr name;
  @attr placeholder;

  @belongsTo("service", {async: false, inverse: null}) service
}
