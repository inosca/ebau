import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class LegalSubmissionEditAppealRoute extends Route {
  @service ebauModules;

  model({ document_uuid: documentId }) {
    return { documentId, instanceId: this.ebauModules.instanceId };
  }
}
