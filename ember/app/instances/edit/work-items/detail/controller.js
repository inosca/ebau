import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";

export default class WorkItemsInstanceEditController extends Controller {
  @service router;

  @action
  async completeWorkItem() {
    await this.model.completeWorkItem.perform();
  }
}
