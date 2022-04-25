import Model, { attr } from "@ember-data/model";

export default class AuthorityModel extends Model {
  @attr authorityId;
  @attr name;
}
