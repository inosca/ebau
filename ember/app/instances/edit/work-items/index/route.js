import Route from "@ember/routing/route";

export default class InstancesEditWorkItemsIndexRoute extends Route {
  afterModel(model) {
    if (model.meta["access-type"] === "public") {
      this.transitionTo("instances.edit.index");
    }
  }

  model() {
    return this.modelFor("instances.edit");
  }
}
