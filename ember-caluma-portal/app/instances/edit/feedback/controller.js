import Controller, { inject as controller } from "@ember/controller";

export default class InstancesEditFeedbackController extends Controller {
  @controller("instances.edit") editController;

  get loading() {
    return this.editController.feeback.isRunning;
  }

  get feedback() {
    return this.editController.feedback.value;
  }
}
