import Route from "@ember/routing/route";

export default class CasesDetailWorkItemsNewRoute extends Route {
  model() {
    return this.modelFor("cases.detail");
  }
}
