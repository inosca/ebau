import Model, { attr } from "@ember-data/model";

export default class AccessLevelModel extends Model {
  @attr slug;
  @attr requiredGrantType;
}
