import Route from "@ember/routing/route";
import { service } from "@ember/service";

import mainConfig from "ember-ebau-core/config/main";

export default class ServicePermissionsIndexRoute extends Route {
  @service router;
  @service ebauModules;

  get defaultRoute() {
    return mainConfig.servicePermissions?.includeSubRoutes[0] || "permissions";
  }

  redirect() {
    this.router.replaceWith(
      this.ebauModules.resolveModuleRoute(
        "service-permissions",
        this.defaultRoute,
      ),
    );
  }
}
