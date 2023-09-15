import Controller from "@ember/controller";
import { action } from "@ember/object";
import { tracked } from "@glimmer/tracking";

export default class WorkItemsIndexController extends Controller {
  queryParams = ["order", "responsible", "type", "status", "role"];

  // Filters
  @tracked order = "urgent";
  @tracked responsible = "all";
  @tracked type = "all";
  @tracked role = "active";
  @tracked status = "READY";

  @action
  setFilter(filter, value) {
    this[filter] = value;
  }
}
