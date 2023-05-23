import Controller from "@ember/controller";
import { inject as service } from "@ember/service";

export default class ServicePermissionsOrganisationController extends Controller {
  @service ebauModules;

  get isMunicipality() {
    return this.ebauModules.baseRole === "municipality";
  }
}
