import { computed } from "@ember/object";
import { reads } from "@ember/object/computed";
import Service, { inject as service } from "@ember/service";
import fetch from "fetch";

export default class FetchService extends Service {
  @service session;

  @reads("session.data.authenticated.access_token") token;
  @reads("session.language") language;
  @reads("session.group") group;

  @computed("token", "group")
  get headers() {
    return {
      authorization: `Bearer ${this.token}`,
      accept: "application/vnd.api+json",
      "content-type": "application/vnd.api+json",
      "accept-language": this.language,
      ...(this.group ? { "x-camac-group": this.group } : {})
    };
  }

  async fetch(resource, init = {}) {
    init.headers = Object.assign({}, this.headers, init.headers);

    // clean out undefined headers
    Object.keys(init.headers).forEach(
      k => init.headers[k] === undefined && delete init.headers[k]
    );

    const response = await fetch(resource, init);

    if (!response.ok) {
      // invalidate the session on 401 requests
      if (response.status === 401 && this.session.isAuthenticated) {
        this.session.invalidate();
      }

      const contentType = response.headers.map["content-type"];
      let body = "";

      if (/^application\/(vnd\.api+)?json$/.test(contentType)) {
        body = await response.json();
      } else if (contentType === "text/plain") {
        body = await response.text();
      }

      // throw an error containing a human readable message
      throw new Error(
        `Fetch request to URL ${response.url} returned ${response.status} ${response.statusText}:\n\n${body}`
      );
    }

    return response;
  }
}
