import Model, { attr, belongsTo } from "@ember-data/model";

export default class ActivationModel extends Model {
  @attr deadlineDate;
  @attr suspensionDate;
  @attr endDate;
  @attr state;

  @belongsTo("circulation", { inverse: "activations", async: true })
  circulation;
  @belongsTo("service", { inverse: "activations", async: true }) service;
}
