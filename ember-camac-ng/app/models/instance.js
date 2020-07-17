import Model, { attr, belongsTo } from "@ember-data/model";

export default class InstanceModel extends Model {
  @attr("string") identifier;
  @belongsTo("form") form;
}
