import Model, { attr } from "@ember-data/model";

export default class WorkItemTemplateModel extends Model {
  @attr name;
  @attr description;
  @attr leadTime;
  @attr responsibilityRule;
}
