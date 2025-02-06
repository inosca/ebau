import Route from "@ember/routing/route";

export default class SnippetsAdminNewRoute extends Route {
  resetController(controller, isExiting) {
    if (isExiting) {
      controller.category = null;
    }
  }
}
