import Controller from "@ember/controller";
import { action } from "@ember/object";
import { service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import workItemListConfig from "ember-ebau-core/config/work-item-list";

export default class WorkItemsController extends Controller {
  @service session;
  @service intl;
  @service store;

  filterDefaults = workItemListConfig.filterDefaults;
  queryParams = [
    "order",
    "responsible",
    "type",
    "status",
    "role",
    "task",
    "preset",
  ];

  // Filters
  @tracked order = this.filterDefaults.order;
  @tracked responsible = this.filterDefaults.responsible;
  @tracked type = this.filterDefaults.type;
  @tracked role = this.filterDefaults.role;
  @tracked status = this.filterDefaults.status;
  @tracked task = this.filterDefaults.task;
  @tracked preset = this.filterDefaults.preset;

  @action
  setFilter(filter, value) {
    this[filter] = value;
  }
}
