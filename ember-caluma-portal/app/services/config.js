import { tracked } from "@glimmer/tracking";
import ConfigService from "ember-alexandria/services/config";

export default class AlexandriaConfigService extends ConfigService {
  @tracked instanceId;

  get defaultModelMeta() {
    return {
      case_id: this.instanceId,
    };
  }
}