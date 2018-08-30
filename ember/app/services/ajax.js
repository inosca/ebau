import AjaxService from "ember-ajax/services/ajax";
import { inject as service } from "@ember/service";
import { computed } from "@ember/object";
import { reads } from "@ember/object/computed";
import { UnauthorizedError } from "ember-ajax/errors";

export default AjaxService.extend({
  session: service(),

  token: reads("session.data.authenticated.access_token"),

  headers: computed("token", function() {
    let token = this.token;

    return token ? { Authorization: `Bearer ${token}` } : {};
  }),

  handleResponse() {
    let res = this._super(...arguments);

    if (
      res instanceof UnauthorizedError &&
      this.get("session.isAuthenticated")
    ) {
      this.session.invalidate();
    }

    return res;
  }
});
