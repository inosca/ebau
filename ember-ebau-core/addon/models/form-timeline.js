import Model, { attr, belongsTo } from "@ember-data/model";

export default class FormFieldModel extends Model {
  @attr("string") timelineType;
  @attr("string") label;
  @attr("date") startDate;
  @attr("date") endDate;

  @belongsTo("instance", { inverse: null, async: true }) instance;
}
