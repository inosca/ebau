import Model, { attr, belongsTo } from "@ember-data/model";

export default class GisLinkModel extends Model {
  @attr name;
  @attr placeholder;
  @attr gisLinkForInstance;

  @belongsTo("service", { async: false, inverse: null }) service;
}
