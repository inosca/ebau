import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class ProtectedRoute extends Route {
  @service session;
  @service permissions;

  async beforeModel(transition) {
    await this.session.requireAuthentication(transition, "login");
    await this.session._data.promise;
    if (this.session.isAuthenticated) {
      await this.permissions.setup();
    }
  }
}
