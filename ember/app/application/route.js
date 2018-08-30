import Route from "@ember/routing/route";
import ApplicationRouteMixin from "ember-simple-auth/mixins/application-route-mixin";

export default Route.extend(ApplicationRouteMixin, {
  sessionAuthenticated() {
    let next = this.get("session.data.next");

    if (next) {
      return this.transitionTo(next);
    }

    return this._super(...arguments);
  }
});
