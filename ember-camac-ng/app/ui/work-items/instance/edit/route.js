import Route from "@ember/routing/route";

export default class WorkItemsInstanceEditRoute extends Route {
  model({ work_item_id: id }) {
    return id;
  }
}
