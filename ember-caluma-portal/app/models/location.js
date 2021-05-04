import Model, { attr } from "@ember-data/model";

export default class Location extends Model {
  @attr name;
  @attr communalFederalNumber;
}
