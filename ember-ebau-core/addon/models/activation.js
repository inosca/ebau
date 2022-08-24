import Model, { attr, belongsTo } from "@ember-data/model";

export default class ActivationModel extends Model {
  @attr deadlineDate;
  @attr suspensionDate;
  @attr endDate;
  @attr state;

  @belongsTo circulation;
  @belongsTo service;
}
