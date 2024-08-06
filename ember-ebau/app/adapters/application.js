import OIDCJSONAPIAdapter from "ember-simple-auth-oidc/adapters/oidc-json-api-adapter";

export default class ApplicationAdapter extends OIDCJSONAPIAdapter {
  get namespace() {
    // this needs to be a getter instead of a property in order for
    // ember-alexandria to override it with a getter in their adapters
    return "api/v1";
  }

  _appendInclude(url, adapterOptions) {
    if (adapterOptions?.include) {
      return `${url}?include=${adapterOptions.include}`;
    }

    return url;
  }

  urlForUpdateRecord(...args) {
    const [, , { adapterOptions }] = args;

    return this._appendInclude(
      super.urlForUpdateRecord(...args),
      adapterOptions,
    );
  }

  urlForCreateRecord(...args) {
    const [, { adapterOptions }] = args;

    return this._appendInclude(
      super.urlForCreateRecord(...args),
      adapterOptions,
    );
  }
}
