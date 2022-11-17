import Route from "@ember/routing/route";

export default class LegalSubmissionIndexRoute extends Route {
  model() {
    return this.modelFor("legal-submission");
  }
}
