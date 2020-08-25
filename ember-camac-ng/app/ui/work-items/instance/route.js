import Route from "@ember/routing/route";

export default class WorkItemsInstanceRoute extends Route {
  model({ id }) {
    return id;
  }
}
