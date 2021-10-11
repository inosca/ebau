import Route from "@ember/routing/route";

export default class PublicInstancesDetailRoute extends Route {
  queryParams = { key: { refresh: true } };

  model({ instance_id }) {
    return parseInt(instance_id);
  }

  resetController(controller, isExiting) {
    if (isExiting) {
      controller.key = null;
    }
  }

  setupController(controller, model) {
    super.setupController(controller, model);

    controller.fetchPublicInstance.perform();
  }
}
