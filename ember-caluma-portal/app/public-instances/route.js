import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

import config from "caluma-portal/config/environment";

export default class PublicInstancesRoute extends Route {
  @service session;

  activate() {
    this.session.enforcePublicAccess = true;
  }

  deactivate() {
    this.session.enforcePublicAccess = false;
  }

  beforeModel(transition) {
    if (config.APPLICATION.name === "be") {
      this.session.requireAuthentication(transition, "login");
    }
  }
}
