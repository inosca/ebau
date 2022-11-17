import Route from "@ember/routing/route";

export default class LegalSubmissionEditRoute extends Route {
  model({ document_uuid }) {
    return document_uuid;
  }
}
