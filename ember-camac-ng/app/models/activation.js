import Model, { attr, belongsTo } from "@ember-data/model";

export default class ActivationModel extends Model {
  @attr deadlineDate;
  @attr state;

  @belongsTo circulation;
}
