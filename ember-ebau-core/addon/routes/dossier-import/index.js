import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class DossierImportIndexRoute extends Route {
  @service ebauModules;

  model() {
    return this.ebauModules.serviceId;
  }

  setupController(controller, model) {
    super.setupController(controller, model);
    controller.fetchImports.perform();
  }
}
