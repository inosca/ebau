import JSONAPIAdapter from "@ember-data/adapter/json-api";
import { inject as service } from "@ember/service";
import oidcConfig from "ember-simple-auth-oidc/config";
import OIDCAdapterMixin from "ember-simple-auth-oidc/mixins/oidc-adapter-mixin";

const BaseAdapter = JSONAPIAdapter.extend(OIDCAdapterMixin);

const { authHeaderName, authPrefix, tokenPropertyName } = oidcConfig;

export default class ApplicationAdapter extends BaseAdapter {
  @service session;

  namespace = "api/v1";

  get headers() {
    const token = this.session.data.authenticated[tokenPropertyName];
    const tokenKey = authHeaderName.toLowerCase();

    return {
      ...(token ? { [tokenKey]: `${authPrefix} ${token}` } : {}),
      ...(this.session.data.enforcePublicAccess
        ? { "x-camac-public-access": true }
        : {}),
    };
  }
}
