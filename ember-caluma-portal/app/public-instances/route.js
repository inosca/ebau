import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";

export default class PublicInstancesRoute extends Route {
  @service session;

  activate() {
    this.session.enforcePublicAccess = true;
  }

  deactivate() {
    this.session.enforcePublicAccess = false;
  }

  beforeModel(transition) {
    if (!hasFeature("publication.disableAuthentication")) {
      this.session.requireAuthentication(transition, "login");
    }
  }
}
