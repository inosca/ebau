import Route from "@ember/routing/route";

export default class PublicInstancesIndexRoute extends Route {
  setupController(controller, model) {
    super.setupController(controller, model);

    controller.fetchInstances.perform();
  }

  resetController(controller, isExiting, transition) {
    super.resetController(controller, isExiting, transition);

    if (isExiting) {
      controller.page = 1;
      controller.instances = [];
    }
  }
}
