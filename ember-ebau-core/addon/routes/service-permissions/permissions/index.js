import Route from "@ember/routing/route";

export default class ServicePermissionsPermissionsIndexRoute extends Route {
  resetController(controller, isExiting, transition) {
    super.resetController(controller, isExiting, transition);

    if (isExiting) {
      controller.search = "";
      controller.page = 1;
    }
  }
}
