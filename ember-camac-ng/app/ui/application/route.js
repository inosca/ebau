import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";
// eslint-disable-next-line ember/no-mixins
import ApplicationRouteMixin from "ember-simple-auth/mixins/application-route-mixin";

const ApplicationRouteBase = Route.extend(ApplicationRouteMixin);

export default class ApplicationRoute extends ApplicationRouteBase {
  @service intl;
  @service session;
  @service shoebox;

  async beforeModel(...args) {
    super.beforeModel(...args);

    if (!this.session.isAuthenticated) {
      await this.session.authenticate("authenticator:camac");
    }

    this.intl.setLocale(this.shoebox.content.language);
  }

  sessionInvalidated() {
    this.session.authenticate("authenticator:camac");
  }
}
