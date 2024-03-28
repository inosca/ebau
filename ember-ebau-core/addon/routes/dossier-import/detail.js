import { action } from "@ember/object";
import Route from "@ember/routing/route";

export default class DossierImportDetailRoute extends Route {
  model(params) {
    return params.import_id;
  }

  setupController(controller, model) {
    super.setupController(controller, model);
    controller.fetchImport.perform();
  }

  /**
   * In future versions a component would provide a better solution
   * for refreshing the import without having to disable the linter rule.
   */

  @action
  didTransition() {
    // eslint-disable-next-line ember/no-controller-access-in-routes
    const controller = this.controllerFor("dossier-import.detail");
    controller.refresh.perform();
    return true;
  }

  @action
  willTransition() {
    // eslint-disable-next-line ember/no-controller-access-in-routes
    const controller = this.controllerFor("dossier-import.detail");
    controller.refresh.cancelAll();
    return true;
  }
}
