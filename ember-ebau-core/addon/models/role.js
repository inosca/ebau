import Model, { attr } from "@ember-data/model";

export default class Role extends Model {
  @attr("string") name;
  @attr("string") permission;
}
