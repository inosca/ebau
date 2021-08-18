import Route from "@ember/routing/route";

export default class PublicInstancesIndexRoute extends Route {
  queryParams = {
    municipality: { refresh: true },
  };

  setupController(controller, model) {
    super.setupController(controller, model);

    controller.fetchMunicipalities.perform();
    controller.fetchInstances.perform();
  }

  resetController(controller, isExiting, transition) {
    super.resetController(controller, isExiting, transition);

    if (isExiting) {
      controller.reset();
    }
  }
}
