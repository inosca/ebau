import Route from "@ember/routing/route";

export default class BillingIndexRoute extends Route {
  setupController(controller, model) {
    super.setupController(controller, model);
    if (controller.entries.hasRan) {
      controller.entries.retry();
    }
  }
}
