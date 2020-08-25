import Route from "@ember/routing/route";

export default class WorkItemListInstanceRoute extends Route {
  model({ id }) {
    return id;
  }
}
