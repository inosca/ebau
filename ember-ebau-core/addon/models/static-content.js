import Model, { attr } from "@ember-data/model";

export default class StaticContentModel extends Model {
  @attr content;
  @attr slug;
}
