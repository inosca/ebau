import Route from "@ember/routing/route";

export default class FormRoute extends Route {
  setupController(controller, model) {
    super.setupController(controller, model);
    controller.getData.perform();
  }
}
