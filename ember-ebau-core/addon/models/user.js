import Model, { attr, belongsTo, hasMany } from "@ember-data/model";

export default class UserModel extends Model {
  @attr name;
  @attr surname;
  @attr username;
  @attr email;

  @belongsTo("service", { inverse: "users", async: true }) service;
  @belongsTo("group", { inverse: null, async: true }) defaultGroup;
  @hasMany("group", { inverse: null, async: true }) groups;

  get fullName() {
    return `${this.name} ${this.surname}`;
  }
}
