import Route from "@ember/routing/route";

export default class AuditIndexRoute extends Route {
  model() {
    return this.modelFor("audit");
  }
}
