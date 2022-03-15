import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";
export default class InstancesRoute extends Route {
  @service session;

  async model() {
    this.session.set("data.enforcePublicAccess", false);
  }
}
