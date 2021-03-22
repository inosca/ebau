import JSONAPIAdapter from "@ember-data/adapter/json-api";
import { inject as service } from "@ember/service";

export default class ApplicationAdapter extends JSONAPIAdapter {
  namespace = "api/v1";

  @service session;

  get headers() {
    return this.session.headers;
  }

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

  handleResponse(status, ...args) {
    if (status === 401 && this.session.isAuthenticated) {
      this.session.invalidate();
    }

    return super.handleResponse(status, ...args);
  }
}
