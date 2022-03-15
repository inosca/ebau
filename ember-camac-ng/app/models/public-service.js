import Model, { attr } from "@ember-data/model";

export default class PublicService extends Model {
  @attr("string") name;
}
