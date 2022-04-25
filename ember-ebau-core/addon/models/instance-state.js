import Model, { attr } from "@ember-data/model";

export default class InstanceStateModel extends Model {
  @attr name;
  @attr description;

  get uppercaseName() {
    return this.name.toUpperCase();
  }
}
