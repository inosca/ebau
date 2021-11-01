import Route from "@ember/routing/route";

export default class CasesDashboardRoute extends Route {
  model() {
    return this.modelFor("cases.detail");
  }
}
