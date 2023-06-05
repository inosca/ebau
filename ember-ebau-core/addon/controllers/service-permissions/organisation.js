import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { macroCondition, getOwnConfig } from "@embroider/macros";

export default class ServicePermissionsOrganisationController extends Controller {
  @service ebauModules;

  get showResponsibilityConstructionControl() {
    if (macroCondition(getOwnConfig().hasBuildingControl)) {
      return this.ebauModules.baseRole === "municipality";
    }
    return false;
  }
}
