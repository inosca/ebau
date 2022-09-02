import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";

export default class WorkItemsInstanceIndexController extends Controller {
  queryParams = ["role"];

  @service shoebox;

  @tracked role = "active";

  @action
  setFilter(filter, value) {
    this[filter] = value;
  }
}
