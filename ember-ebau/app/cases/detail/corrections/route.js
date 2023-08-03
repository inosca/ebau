import Route from "@ember/routing/route";

export default class CorrectionsRoute extends Route {
  model() {
    return this.modelFor("cases.detail");
  }
}
