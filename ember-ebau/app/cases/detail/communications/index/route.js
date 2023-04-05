import Route from "@ember/routing/route";

export default class ProtectedCasesDetailCommunicationsIndexRoute extends Route {
  model() {
    return this.modelFor("cases.detail");
  }
}
