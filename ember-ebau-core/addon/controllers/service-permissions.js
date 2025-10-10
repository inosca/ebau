import Controller from "@ember/controller";

import mainConfig from "ember-ebau-core/config/main";

export default class ServicePermissionsController extends Controller {
  get hasMoreThenOneRoute() {
    return this.includeSubRoutes.length > 1;
  }

  get includeSubRoutes() {
    return (
      mainConfig.servicePermissions?.includeSubRoutes || [
        "permissions",
        "invitations",
        "organisation",
        "sub-services",
      ]
    );
  }
}
