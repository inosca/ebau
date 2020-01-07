import Model, { attr } from "@ember-data/model";

export default class PublicRole extends Model {
  @attr("string") name;
}
