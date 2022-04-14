import Model, { attr } from "@ember-data/model";

export default class TagModel extends Model {
  @attr name;
}
