import Route from "@ember/routing/route";

export default class CasesDetailDmsGenerateRoute extends Route {
  model() {
    return this.modelFor("cases.detail");
  }
}
