import Route from "@ember/routing/route";
import OIDCApplicationRouteMixin from "ember-simple-auth-oidc/mixins/oidc-application-route-mixin";
import moment from "moment";

export default Route.extend(OIDCApplicationRouteMixin, {
  sessionAuthenticated() {
    let next = this.get("session.data.next");

    if (next) {
      return this.transitionTo(next);
    }

    return this._super(...arguments);
  },

  beforeModel() {
    moment.locale("de-ch");
  }
});
