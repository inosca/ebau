import JSONAPIAdapter from "@ember-data/adapter/json-api";
import DataAdapterMixin from "ember-simple-auth/mixins/data-adapter-mixin";
import { inject as service } from "@ember/service";
import { reads } from "@ember/object/computed";

export default class ApplicationAdapter extends JSONAPIAdapter.extend(
  DataAdapterMixin
) {
  namespace = "api/v1";

  @service session;
  @service router;

  @reads("session.data.authenticated.access_token") token;
  @reads("router.currentRoute.queryParams.group") group;

  authorize(request) {
    if (this.token) {
      request.setRequestHeader("authorization", `Bearer ${this.token}`);
    }

    if (this.group) {
      request.setRequestHeader("x-camac-group", this.group);
    }
  }

  _appendInclude(url, adapterOptions) {
    if (adapterOptions && adapterOptions.include) {
      return `${url}?include=${adapterOptions.include}`;
    }
  }

  urlForUpdateRecord(_, { adapterOptions }) {
    return this._appendInclude(
      super.urlForUpdateRecord(...arguments),
      adapterOptions
    );
  }

  urlForCreateRecord(_, { adapterOptions }) {
    return this._appendInclude(
      super.urlForCreateRecord(...arguments),
      adapterOptions
    );
  }
}
