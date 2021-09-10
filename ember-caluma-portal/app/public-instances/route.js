import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class PublicInstancesRoute extends Route {
  @service session;

  activate() {
    this.session.enforcePublicAccess = true;
  }

  deactivate() {
    this.session.enforcePublicAccess = false;
  }
}
