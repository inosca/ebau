import Model, { attr, belongsTo } from "@ember-data/model";

export default class SanctionTemplate extends Model {
  @attr name;
  @attr description;
  @attr controlStep;

  @belongsTo("service", { async: false, inverse: null }) createdByService;
  @belongsTo("service", { async: false, inverse: null }) assignedService;
}
