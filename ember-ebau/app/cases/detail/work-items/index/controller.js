import Controller from "@ember/controller";
import { action } from "@ember/object";
import { tracked } from "@glimmer/tracking";

export default class CasesDetailWorkItemsIndexController extends Controller {
  queryParams = ["role"];

  @tracked role = "active";

  @action
  setFilter(filter, value) {
    this[filter] = value;
  }
}
