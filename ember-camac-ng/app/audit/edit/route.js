import Route from "@ember/routing/route";

export default class AuditEditRoute extends Route {
  model({ document_uuid: documentUuid }) {
    return documentUuid;
  }
}
