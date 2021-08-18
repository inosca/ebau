import Route from "@ember/routing/route";

export default class PublicInstancesDetailRoute extends Route {
  model({ instance_id }) {
    return parseInt(instance_id);
  }

  setupController(controller, model) {
    super.setupController(controller, model);

    controller.fetchPublicInstance.perform();
  }
}
