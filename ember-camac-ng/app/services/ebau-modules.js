import { inject as service } from "@ember/service";
import EbauModulesService from "ember-ebau-core/services/ebau-modules";

export default class CustomEbauModulesService extends EbauModulesService {
  @service shoebox;

  get serviceId() {
    return this.shoebox.content.serviceId;
  }
}
