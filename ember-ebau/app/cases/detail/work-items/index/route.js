import Route from "@ember/routing/route";

export default class CasesDetailWorkItemsIndexRoute extends Route {
  model() {
    return this.modelFor("cases.detail");
  }
}
