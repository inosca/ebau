import Model, { attr, hasMany } from "@ember-data/model";
import { computed } from "@ember/object";

export default class User extends Model {
  @attr("string") name;
  @attr("string") surname;
  @attr("string") username;

  @hasMany("group") groups;

  @computed("name", "surname")
  get fullName() {
    return `${this.surname} ${this.name}`;
  }
}
