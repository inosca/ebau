import Model, { attr, belongsTo, hasMany } from "@ember-data/model";

export default class ResponsibleUserRuleModel extends Model {
  @attr sort;

  @hasMany("application-type", { async: false, inverse: null })
  applicationTypes;
  @hasMany("public-service", { async: false, inverse: null }) municipalities;
  @belongsTo("user", { async: false, inverse: null }) responsibleUser;

  get type() {
    if (this.hasMany("municipalities").ids().length) {
      return "municipalities";
    } else if (this.hasMany("applicationTypes").ids().length) {
      return "application-types";
    }

    // Default for new records
    return "municipalities";
  }
}
