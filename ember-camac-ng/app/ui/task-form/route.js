import Route from "@ember/routing/route";

export default class TaskFormRoute extends Route {
  model(params) {
    return params;
  }

  setupController(controller, model) {
    super.setupController(controller, model);

    controller.fetchWorkItem.perform();
  }
}
