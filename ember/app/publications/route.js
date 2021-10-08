import Route from "@ember/routing/route";

export default class PublicationsRoute extends Route {
  setupController(controller, model) {
    super.setupController(controller, model);
    controller.fetchPublications.perform();
  }

  resetController(controller, isExiting, transition) {
    super.resetController(controller, isExiting, transition);

    if (isExiting) {
      controller.reset();
    }
  }
}
