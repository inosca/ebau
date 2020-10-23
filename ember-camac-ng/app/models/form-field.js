import Model, { attr, belongsTo } from "@ember-data/model";

export default class FormFieldModel extends Model {
  @attr("string") name;
  @attr value;

  @belongsTo instance;
}
