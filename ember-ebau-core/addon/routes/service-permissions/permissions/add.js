import Route from "@ember/routing/route";

export default class ServicePermissionsPermissionsAddRoute extends Route {
  setupController(controller, model) {
    super.setupController(controller, model);
    if (controller.groups.hasRan) {
      controller.groups.retry();
    }
  }
}
