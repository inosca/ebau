import Model, { attr, belongsTo } from "@ember-data/model";

export default class DeadlinesInstanceDeadlineModel extends Model {
  @attr name;
  @attr("date") startDate;
  @attr("date") processDeadlineDate;
  @attr("number") processDeadlineDays;
  @attr("number") totalDaysOfSuspension;

  @belongsTo("deadline-type", {
    inverse: null,
    async: true,
  })
  deadlineType;
  @belongsTo("service", { inverse: null, async: true }) service;
  @belongsTo("instance", { inverse: null, async: true }) instance;
}
