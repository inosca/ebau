import Route from "@ember/routing/route";

export default class CasesNewRoute extends Route {
  resetController(controller, isExiting) {
    if (isExiting) {
      controller.selectedForm = null;
    }
  }

  setupController(controller, model) {
    super.setupController(controller, model);
    controller.fetchForms.perform();
  }
}
