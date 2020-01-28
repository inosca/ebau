import Model, { attr } from "@ember-data/model";
import { computed } from "@ember/object";

export default class User extends Model {
  @attr("string") name;
  @attr("string") surname;
  @attr("string") username;

  @computed("name", "surname")
  get fullName() {
    return `${this.surname} ${this.name}`;
  }
}
