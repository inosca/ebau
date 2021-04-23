import Route from "@ember/routing/route";

export default class PublicInstancesIndexRoute extends Route {
  setupController(controller, model) {
    super.setupController(controller, model);
    controller.getPublicInstances.perform();
  }
}
