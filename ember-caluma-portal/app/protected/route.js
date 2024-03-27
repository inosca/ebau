import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

import config from "caluma-portal/config/environment";

export default class ProtectedRoute extends Route {
  @service session;

  beforeModel(transition) {
    this.session.requireAuthentication(
      transition,
      config["ember-simple-auth-oidc"].afterLogoutUri,
    );
  }
}
