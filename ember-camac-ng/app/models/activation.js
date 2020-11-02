import Model, { attr } from "@ember-data/model";

export default class ActivationModel extends Model {
  @attr deadlineDate;
  @attr state;
}
