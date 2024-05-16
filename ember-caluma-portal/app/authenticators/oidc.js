import { getConfig } from "@embroider/macros";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";
import OidcAuthenticator from "ember-simple-auth-oidc/authenticators/oidc";
import getAbsoluteUrl from "ember-simple-auth-oidc/utils/absolute-url";

export default class extends OidcAuthenticator {
  restore(sessionData) {
    if (
      hasFeature("login.tokenExchange") &&
      this.session.isAuthenticated &&
      this.session.isTokenExchange &&
      this.session.data.referrer === "internal"
    ) {
      // If we are currently logged in via token exchange but we are coming from
      // ember-ebau we need to destroy the current session in order to be logged
      // in via OIDC
      return this.session.invalidate();
    }

    return super.restore(sessionData);
  }

  singleLogout(idToken) {
    if (!this.session.isTokenExchange) {
      return super.singleLogout(idToken);
    }

    const params = [
      `post_logout_redirect_uri=${getConfig("ember-ebau-core").eGovPortalURL}`,
    ];

    if (idToken) {
      params.push(`id_token_hint=${idToken}`);
    }

    this._redirectToUrl(
      `${getAbsoluteUrl(this.config.endSessionEndpoint, this.config.host)}?${params.join("&")}`,
    );
  }
}
