import { tracked } from "@glimmer/tracking";
import AlexandriaConfigService from "ember-alexandria/services/alexandria-config";

export default class CustomAlexandriaConfigService extends AlexandriaConfigService {
  @tracked instanceId;
  @tracked documentId;

  namespace = "alexandria/api/v1";

  get defaultModelMeta() {
    return {
      document: {
        "camac-instance-id": String(this.instanceId),
        "caluma-document-id": this.documentId,
      },
    };
  }
}
