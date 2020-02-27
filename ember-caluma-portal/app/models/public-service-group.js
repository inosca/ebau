import Model, { attr } from "@ember-data/model";

export default class PublicServiceGroup extends Model {
  @attr("string") name;
}
