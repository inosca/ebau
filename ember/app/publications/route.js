import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class PublicationsRoute extends Route {
  @service session;

  setupController(controller, model) {
    super.setupController(controller, model);
    this.session.set("data.enforcePublicAccess", true);
    controller.fetchPublications.perform();
  }

  resetController(controller, isExiting, transition) {
    super.resetController(controller, isExiting, transition);

    if (isExiting) {
      controller.reset();
    }
  }
}
