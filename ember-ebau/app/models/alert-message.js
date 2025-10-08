import Model, { attr } from "@ember-data/model";

export default class AlertMessageModel extends Model {
  @attr("string") title;
  @attr("date") createdAt;
  @attr("date") updatedAt;
  @attr("boolean") active;
  @attr("date") startDate;
  @attr("date") endDate;
  @attr("string") message;
}
