import Route from "@ember/routing/route";

export default class InstancesEditWorkItemsDetailRoute extends Route {
  model(workItem) {
    return workItem;
  }
}
