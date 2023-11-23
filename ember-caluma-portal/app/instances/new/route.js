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
}
