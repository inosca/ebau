import Controller from "@ember/controller";
import { reads } from "@ember/object/computed";
import { inject as controller } from "@ember/controller";

export default Controller.extend({
  editController: controller("instances.edit"),
  loading: reads("editController.feedbackTask.isRunning"),
  feedback: reads("editController.feedback")
});
