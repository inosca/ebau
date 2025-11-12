import { service } from "@ember/service";
import CustomAlexandriaConfigService from "ember-ebau-core/services/alexandria-config";

export default class extends CustomAlexandriaConfigService {
  @service shoebox;

  get instanceId() {
    return this.shoebox.content.instanceId;
  }
}
