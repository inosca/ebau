import Route from "@ember/routing/route";

export default class CasesDetailFormRoute extends Route {
  model() {
    return this.modelFor("cases.detail");
  }
}
