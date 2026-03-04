import Model, { attr, belongsTo } from "@ember-data/model";

export default class DeadlinesSuspensionModel extends Model {
  @attr("date") startDate;
  @attr("date") endDate;
  @attr reason;
  @attr reasonText;
  @attr reasonFormatted;
  @attr authorFormatted;

  @belongsTo("instance-deadline", { inverse: null, async: true }) deadline;
  @belongsTo("group", { inverse: null, async: true, readOnly: true }) group;
  @belongsTo("user", { inverse: null, async: true, readOnly: true }) user;
}
