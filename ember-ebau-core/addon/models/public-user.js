import Model, { attr } from "@ember-data/model";

export default class PublicUser extends Model {
  @attr("string") name;
  @attr("string") surname;
  @attr("string") username;

  get fullName() {
    return `${this.name} ${this.surname}`;
  }
}
