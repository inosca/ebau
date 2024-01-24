import Route from "@ember/routing/route";

export default class InstancesEditApplicantsRoute extends Route {
  setupController(controller, model) {
    super.setupController(controller, model);
    if (controller.currentMunicipality.hasRan) {
      controller.currentMunicipality.reload();
    }
  }
}
