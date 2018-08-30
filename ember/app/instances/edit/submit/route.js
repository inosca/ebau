import Route from "@ember/routing/route";

export default Route.extend({
  setupController(controller) {
    this._super(...arguments);

    // canSubmit is computed off a service. It should be triggered while the
    // route is not active but somehow isn't. This is why we trigger the
    // property manually here
    controller.notifyPropertyChange("canSubmit");
  }
});
