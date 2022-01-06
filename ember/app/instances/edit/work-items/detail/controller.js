import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";

export default class WorkItemsInstanceEditController extends Controller {
  @service router;

  @action
  async completeWorkItem() {
    await this.model.completeWorkItem.perform();

    await this.router.transitionTo("instance.edit.work-items.index");
  }
}
