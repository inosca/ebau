import Model, { attr } from "@ember-data/model";

export default class DeadlinesSuspensionReasonModel extends Model {
  @attr("string") label;
  @attr("string") code;
}
