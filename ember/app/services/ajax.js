import { computed } from "@ember/object";
import { reads } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import { UnauthorizedError } from "ember-ajax/errors";
import AjaxService from "ember-ajax/services/ajax";

export default AjaxService.extend({
  session: service(),

  router: service(),

  token: reads("session.data.authenticated.access_token"),

  headers: computed("token", function() {
    const token = this.token;

    return token ? { Authorization: `Bearer ${token}` } : {};
  }),

  handleResponse(...args) {
    const res = this._super(...args);

    if (res instanceof UnauthorizedError) {
      this.router.transitionTo("logout");
    }

    return res;
  }
});
