import Model, { attr, belongsTo } from "@ember-data/model";

export default class UserModel extends Model {
  @attr name;
  @attr surname;
  @attr username;

  @belongsTo service;

  get fullName() {
    return `${this.name} ${this.surname}`;
  }
}
