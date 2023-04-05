import Route from "@ember/routing/route";

export default class CasesDetailCommunicationsNewRoute extends Route {
  model() {
    return this.modelFor("cases.detail");
  }
}
