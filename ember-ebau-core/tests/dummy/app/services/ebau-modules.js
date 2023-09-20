import { tracked } from "@glimmer/tracking";

import EbauModulesService from "ember-ebau-core/services/ebau-modules";

export default class CustomEbauModulesService extends EbauModulesService {
  @tracked serviceId = null;
  @tracked isApplicant = null;

  reset() {
    this.serviceId = null;
    this.isApplicant = null;
  }
}
