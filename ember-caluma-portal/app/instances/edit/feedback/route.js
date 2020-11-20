import Route from "@ember/routing/route";

import { can } from "ember-caluma-portal/-private/decorators";

@can("read feedback of instance", {
  model: "controller.editController.instance",
  loading: "controller.editController.instanceTask.isRunning",
})
class InstancesEditFeedbackRoute extends Route {}

export default InstancesEditFeedbackRoute;
