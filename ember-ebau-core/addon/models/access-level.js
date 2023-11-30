import Model, { attr } from "@ember-data/model";

export default class AccessLevelModel extends Model {
  @attr name;
  @attr description;
  @attr slug;
  @attr requiredGrantType;
}
