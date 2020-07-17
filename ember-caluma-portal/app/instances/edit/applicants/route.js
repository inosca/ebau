import Route from "@ember/routing/route";
import { can } from "ember-caluma-portal/-private/decorators";

@can("manage applicants of instance", {
  model: "controller.editController.instance",
  loading: "controller.editController.instanceTask.isRunning",
})
class InstancesEditApplicantsRoute extends Route {}

export default InstancesEditApplicantsRoute;
