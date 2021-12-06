import Route from "@ember/routing/route";

export default class DossierImportDetailRoute extends Route {
  model(params) {
    return params.import_id;
  }

  setupController(controller, model) {
    super.setupController(controller, model);
    controller.fetchImport.perform();
  }
}
