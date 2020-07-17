import Route from "@ember/routing/route";
import { can } from "ember-caluma-portal/-private/decorators";

@can("read form of instance", {
  model: "controller.instance",
  loading: "controller.getDocument.isRunning",
  additionalAttributes: { form: "controller.document.form" },
})
class InstancesEditFormRoute extends Route {
  model({ form }) {
    return form;
  }
}

export default InstancesEditFormRoute;
