import Model, { attr } from "@ember-data/model";

export default class PublicMunicipalityModel extends Model {
  @attr name;
  @attr website;
  @attr email;
  @attr phone;
}
