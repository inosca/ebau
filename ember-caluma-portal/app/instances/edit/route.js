import Route from "@ember/routing/route";

import { can } from "ember-caluma-portal/-private/decorators";

@can("read instance", {
  model: "controller.instance",
  loading: "controller.instanceTask.isRunning",
})
class InstancesEditRoute extends Route {
  model({ instance }) {
    return parseInt(instance);
  }
}

export default InstancesEditRoute;
