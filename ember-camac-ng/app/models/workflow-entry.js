import Model, { attr, belongsTo } from "@ember-data/model";

export default class WorkflowEntryModel extends Model {
  @attr workflowEntryId;
  @attr workflowDate;
  @attr group;

  @belongsTo instance;
  @belongsTo workflowItem;
}
