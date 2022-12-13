import { inject as service } from "@ember/service";
import EbauModulesService from "ember-ebau-core/services/ebau-modules";

export default class CustomEbauModulesService extends EbauModulesService {
  @service session;

  get serviceId() {
    return this.session.service?.id;
  }
}
