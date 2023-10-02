import Model, { attr, belongsTo } from "@ember-data/model";

export default class WorkflowEntryModel extends Model {
  @attr workflowEntryId;
  @attr workflowDate;
  @attr group;

  @belongsTo("instance", { inverse: null, async: true }) instance;
  @belongsTo("workflow-item", { inverse: null, async: true }) workflowItem;
}
