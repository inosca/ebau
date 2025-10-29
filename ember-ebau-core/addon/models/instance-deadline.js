import Model, { attr, belongsTo } from "@ember-data/model";

export default class DeadlinesInstanceDeadlineModel extends Model {
  @attr name;
  @attr("date") startDate;
  @attr("date") processDeadlineDate;
  @attr("boolean") processDeadlineDateOverride;
  @attr("number") processDeadlineDays;
  @attr("date") targetDeadlineDate;
  @attr("number") totalDaysOfSuspension;

  @belongsTo("deadline-type", {
    inverse: null,
    async: true,
  })
  deadlineType;
  @belongsTo("service", { inverse: null, async: true }) service;
  @belongsTo("instance", { inverse: null, async: true }) instance;
}
