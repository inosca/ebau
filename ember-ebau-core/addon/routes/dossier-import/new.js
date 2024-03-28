import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class DossierImportNewRoute extends Route {
  @service ebauModules;

  model() {
    return this.ebauModules.serviceId;
  }

  setupController(controller, model) {
    super.setupController(controller, model);
    controller.fileUpload = null;
    controller.fetchGroups.perform();
    controller.fetchLocations.perform();
  }
}
