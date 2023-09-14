import { tracked } from "@glimmer/tracking";
import ConfigService from "ember-alexandria/services/config";

export default class AlexandriaConfigService extends ConfigService {
  @tracked instanceId;
  @tracked documentId;

  get defaultModelMeta() {
    return {
      document: {
        "camac-instance-id": this.instanceId,
        "caluma-document-id": this.documentId,
      },
    };
  }
}
