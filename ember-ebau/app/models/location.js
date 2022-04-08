// copied from ember-camac-ng

import Model, { attr, hasMany } from "@ember-data/model";

export default class LocationModel extends Model {
  @attr name;
  @attr communalFederalNumber;

  @hasMany("group") groups;
}
