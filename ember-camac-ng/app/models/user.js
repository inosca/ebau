import Model, { attr, belongsTo } from "@ember-data/model";

export default class UserModel extends Model {
  @attr("string") name;
  @attr("string") surname;
  @attr("string") username;
  @belongsTo("service") service;

  get fullName() {
    return `${this.name} ${this.surname}`;
  }
}
