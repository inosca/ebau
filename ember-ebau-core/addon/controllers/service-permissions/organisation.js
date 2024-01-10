import Controller from "@ember/controller";
import { inject as service } from "@ember/service";

import { hasFeature } from "ember-ebau-core/helpers/has-feature";

export default class ServicePermissionsOrganisationController extends Controller {
  @service ebauModules;

  get showResponsibilityConstructionControl() {
    if (hasFeature("servicePermissions.hasConstructionControl")) {
      return this.ebauModules.baseRole === "municipality";
    }
    return false;
  }
}
