import Model, { attr, belongsTo } from "@ember-data/model";

export default class DistributionDeadlineRuleModel extends Model {
  @attr leadTime;
  @attr deadline;
  @attr excludeHolidays;

  @belongsTo("public-service", { async: false, inverse: null }) targetService;
}
