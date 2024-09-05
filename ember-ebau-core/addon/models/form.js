import Model, { attr, hasMany } from "@ember-data/model";

export default class FormModel extends Model {
  @attr name;
  @attr description;
  @attr slug;

  @hasMany("service-contents", { inverse: null, async: false }) serviceContents;
}
