import JSONAPIAdapter from "@ember-data/adapter/json-api";
import { reads } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import DataAdapterMixin from "ember-simple-auth/mixins/data-adapter-mixin";

export default class ApplicationAdapter extends JSONAPIAdapter.extend(
  DataAdapterMixin
) {
  namespace = "api/v1";

  @service session;
  @service router;
  @service intl;

  @reads("session.data.authenticated.access_token") token;
  @reads("session.group") group;
  @reads("session.language") language;

  authorize(request) {
    if (this.token) {
      request.setRequestHeader("authorization", `Bearer ${this.token}`);
    }

    if (this.group) {
      request.setRequestHeader("x-camac-group", this.group);
    }

    if (this.language) {
      request.setRequestHeader("accept-language", this.language);
    }
  }

  _appendInclude(url, adapterOptions) {
    if (adapterOptions && adapterOptions.include) {
      return `${url}?include=${adapterOptions.include}`;
    }
  }

  urlForUpdateRecord(...args) {
    const [, { adapterOptions }] = args;

    return this._appendInclude(
      super.urlForUpdateRecord(...args),
      adapterOptions
    );
  }

  urlForCreateRecord(...args) {
    const [, { adapterOptions }] = args;

    return this._appendInclude(
      super.urlForCreateRecord(...args),
      adapterOptions
    );
  }
}
