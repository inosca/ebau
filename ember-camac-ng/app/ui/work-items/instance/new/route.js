import Route from "@ember/routing/route";

export default class WorkItemNewRoute extends Route {
  model() {
    return this.modelFor("work-items.instance");
  }
}
