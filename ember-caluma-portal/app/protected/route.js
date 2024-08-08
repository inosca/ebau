import Route from "@ember/routing/route";
import { service } from "@ember/service";

import config from "caluma-portal/config/environment";

export default class ProtectedRoute extends Route {
  @service session;
  @service permissions;

  async beforeModel(transition) {
    await this.session.requireAuthentication(
      transition,
      config["ember-simple-auth-oidc"].afterLogoutUri,
    );
    if (this.session.isAuthenticated) {
      await this.permissions.setup();
    }
  }
}
