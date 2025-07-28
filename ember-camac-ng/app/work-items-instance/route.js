import Route from "@ember/routing/route";

export default class WorkItemsInstanceRoute extends Route {
  model({ instance_id }) {
    return parseInt(instance_id);
  }
}
