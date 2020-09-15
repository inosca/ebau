import Route from "@ember/routing/route";

export default class InstancesEditWorkItemsIndexRoute extends Route {
  model() {
    return this.modelFor("instances.edit");
  }
}
