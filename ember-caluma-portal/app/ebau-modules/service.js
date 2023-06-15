import { inject as service } from "@ember/service";
import EbauModulesService from "ember-ebau-core/services/ebau-modules";

export default class CustomEbauModulesService extends EbauModulesService {
  @service session;

  get serviceId() {
    return this.session.serviceId;
  }

  get isReadOnlyRole() {
    return this.session.isReadOnlyRole;
  }

  get isApplicant() {
    return !this.session.isInternal;
  }
}
