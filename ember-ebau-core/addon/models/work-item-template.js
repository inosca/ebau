import Model, { attr, belongsTo } from "@ember-data/model";

export default class WorkItemTemplateModel extends Model {
  @attr name;
  @attr description;
  @attr leadTime;
  @attr responsibilityRule;
  @belongsTo("public-user", { inverse: null, async: true })
  assignedUser;
}
