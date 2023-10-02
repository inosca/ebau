import Model, { attr, belongsTo } from "@ember-data/model";

export default class UserModel extends Model {
  @attr name;
  @attr surname;
  @attr username;
  @attr email;

  @belongsTo("service", { inverse: "users", async: true }) service;

  get fullName() {
    return `${this.name} ${this.surname}`;
  }
}
