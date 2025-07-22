import Route from "@ember/routing/route";

export default class DmsAdminNewRoute extends Route {
  resetController(controller, isExiting) {
    if (isExiting) {
      controller.set("shared", false);
    }
  }
}
