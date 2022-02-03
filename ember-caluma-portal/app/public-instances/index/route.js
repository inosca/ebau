import Route from "@ember/routing/route";

export default class PublicInstancesIndexRoute extends Route {
  resetController(controller, isExiting) {
    if (isExiting) {
      controller._instances = [];
      controller.municipality = null;
      controller.dossierNr = null;
      controller.excludeInstance = null;
    }
  }
}
