import Route from "@ember/routing/route";

export default class RejectionRoute extends Route {
  setupController(controller, model) {
    super.setupController(controller, model);
    if (controller.validations.hasRan) {
      controller.validations.reload();
    }
  }
}
