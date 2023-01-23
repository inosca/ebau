import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class LegalSubmissionEditRoute extends Route {
  @service ebauModules;

  model({ document_uuid: documentId }) {
    return { documentId, instanceId: this.ebauModules.instanceId };
  }
}
