import Route from "@ember/routing/route";

export default class ServicePermissionsPermissionsIndexRoute extends Route {
  setupController(controller, model) {
    super.setupController(controller, model);
    if (controller.groups.hasRan) {
      controller.groups.retry();
    }
  }

  resetController(controller, isExiting, transition) {
    super.resetController(controller, isExiting, transition);

    if (isExiting) {
      controller.search = "";
      controller.page = 1;
    }
  }
}
