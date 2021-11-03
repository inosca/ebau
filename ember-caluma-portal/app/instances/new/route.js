import Route from "@ember/routing/route";

export default class InstancesNewRoute extends Route {
  queryParams = {
    convertFrom: { refreshModel: true },
  };
  resetController(controller, isExiting) {
    if (isExiting) {
      controller.convertFrom = null;
      controller.selectedForm = null;
    }
  }

  setupController(controller, model) {
    super.setupController(controller, model);
    controller.fetchForms.perform();
    controller.fetchEbauNumber.perform();
  }
}
