import Service, { inject as service } from "@ember/service";
import fetch from "fetch";
import { reads } from "@ember/object/computed";
import { computed } from "@ember/object";

export default Service.extend({
  session: service(),

  token: reads("session.data.authenticated.access_token"),

  headers: computed("token", function() {
    return {
      authorization: `Bearer ${this.token}`,
      accept: "application/vnd.api+json",
      "content-type": "application/vnd.api+json",
      "cache-control": "no-cache"
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
