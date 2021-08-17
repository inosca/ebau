import Route from "@ember/routing/route";

export default class PublicInstancesDetailDocumentsRoute extends Route {
  setupController(controller, model) {
    super.setupController(controller, model);

    controller.fetchPublicAttachments.perform();
  }
}
