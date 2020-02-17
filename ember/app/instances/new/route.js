import Route from "@ember/routing/route";

export default class InstancesNewRoute extends Route {
  model() {
    return this.store.createRecord("instance");
  }

  setupController(controller, model) {
    super.setupController(controller, model);

    controller.groupData.perform();
    controller.forms.perform();
  }
}
