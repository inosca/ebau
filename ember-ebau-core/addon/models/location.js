import Model, { attr, hasMany } from "@ember-data/model";

export default class LocationModel extends Model {
  @attr name;
  @attr communalFederalNumber;
  @attr zip;

  @hasMany("group", { inverse: null, async: true }) groups;
}
