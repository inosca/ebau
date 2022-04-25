import Model, { attr } from "@ember-data/model";

export default class WorkflowItemModel extends Model {
  @attr workflowItemId;
  @attr position;
  @attr name;
  @attr automatical;
  @attr differentColor;
  @attr isWorkflow;
  @attr isBuildingAuthority;
}
