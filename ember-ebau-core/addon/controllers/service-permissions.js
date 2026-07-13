import Controller from "@ember/controller";
import { service } from "@ember/service";

import mainConfig from "ember-ebau-core/config/main";

export default class ServicePermissionsController extends Controller {
  @service ebauModules;

  get hasMoreThenOneRoute() {
    return this.includeSubRoutes.length > 1;
  }

  get includeSubRoutes() {
    const configuredRoutes =
      mainConfig.servicePermissions?.includeSubRoutes?.filter((route) => {
        if (Array.isArray(route.forServiceSlugs)) {
          return route.forServiceSlugs?.includes(this.ebauModules.serviceSlug);
        }
        return true;
      });

    return configuredRoutes;
  }
}
