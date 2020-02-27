import Controller, { inject as controller } from "@ember/controller";
import { reads } from "@ember/object/computed";

export default class InstancesEditFeedbackController extends Controller {
  @controller("instances.edit") editController;
  @reads("editController.feedbackTask.isRunning") loading;
  @reads("editController.feedback") feedback;
}
