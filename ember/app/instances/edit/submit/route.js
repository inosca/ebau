import Route from "@ember/routing/route";

export default class InstancesEditSubmit extends Route {
  setupController(controller, model) {
    super.setupController(controller, model);

    // canSubmit is computed off a service. It should be triggered while the
    // route is not active but somehow isn't. This is why we trigger the
    // property manually here
    controller.notifyPropertyChange("canSubmit");
    controller.set("params", this.paramsFor("instances.edit"));
  }
}
