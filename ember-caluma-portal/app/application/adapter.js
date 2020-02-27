import JSONAPIAdapter from "@ember-data/adapter/json-api";
import { reads } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import DataAdapterMixin from "ember-simple-auth/mixins/data-adapter-mixin";

export default class ApplicationAdapter extends JSONAPIAdapter.extend(
  DataAdapterMixin
) {
  namespace = "api/v1";

  @service session;

  @reads("session.headers") headers;

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
