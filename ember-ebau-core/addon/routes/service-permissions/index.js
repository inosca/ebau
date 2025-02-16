import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class ServicePermissionsIndexRoute extends Route {
  @service router;
  @service ebauModules;

  redirect() {
    this.router.replaceWith(
      this.ebauModules.resolveModuleRoute("service-permissions", "permissions"),
    );
  }
}
