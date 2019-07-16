import Service, { inject as service } from "@ember/service";
import fetch from "fetch";
import { reads } from "@ember/object/computed";
import { computed } from "@ember/object";

export default Service.extend({
  session: service(),
  router: service(),

  token: reads("session.data.authenticated.access_token"),
  group: reads("router.currentRoute.queryParams.group"),
  role: reads("router.currentRoute.queryParams.role"),

  headers: computed("token", "group", "role", function() {
    return {
      authorization: `Bearer ${this.token}`,
      accept: "application/vnd.api+json",
      "content-type": "application/vnd.api+json",
      ...(this.group ? { "x-camac-group": this.group } : {}),
      ...(this.role ? { "x-camac-role": this.role } : {})
    };
  }),

  fetch(resource, init = {}) {
    init.headers = Object.assign({}, this.headers, init.headers);

    Object.keys(init.headers).forEach(
      k => init.headers[k] === undefined && delete init.headers[k]
    );

    return fetch(resource, init);
  }
});
