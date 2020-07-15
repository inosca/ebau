import Model, { attr } from "@ember-data/model";

export default class FormModel extends Model {
  @attr("string") name;
}
