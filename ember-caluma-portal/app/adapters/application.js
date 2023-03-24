import { inject as service } from "@ember/service";
import OIDCJSONAPIAdapter from "ember-simple-auth-oidc/adapters/oidc-json-api-adapter";

export default class ApplicationAdapter extends OIDCJSONAPIAdapter {
  @service session;

  namespace = "api/v1";

  _appendInclude(url, adapterOptions) {
    if (adapterOptions?.include) {
      return `${url}?include=${adapterOptions.include}`;
    }

    return url;
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
