import Route from "@ember/routing/route";

export default class InstancesEditWorkItemsDetailRoute extends Route {
  model({ work_item_id }) {
    return work_item_id;
  }
}
