import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

import { hasFeature } from "caluma-portal/helpers/has-feature";

export default class PublicInstancesRoute extends Route {
  @service session;

  activate() {
    this.session.enforcePublicAccess = true;
  }

  deactivate() {
    this.session.enforcePublicAccess = false;
  }

  redirect() {
    if (!hasFeature("publication.list")) {
      this.replaceWith("index");
    }
  }
}
