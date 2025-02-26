import Model, { attr, belongsTo } from "@ember-data/model";

export default class Sanction extends Model {
  @attr name;
  @attr description;
  @attr controlStep;
  @attr controlledAt;
  @attr controlNotes;

  @belongsTo("service", { async: false, inverse: null }) createdByService;
  @belongsTo("instance", { async: false, inverse: null }) instance;
  @belongsTo("service", { async: false, inverse: null }) assignedService;
  @belongsTo("user", { async: false, inverse: null }) controlledByUser;

  get controlled() {
    return !!this.controlledAt;
  }
}
