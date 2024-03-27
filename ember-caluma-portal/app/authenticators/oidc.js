import { hasFeature } from "ember-ebau-core/helpers/has-feature";
import OidcAuthenticator from "ember-simple-auth-oidc/authenticators/oidc";

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
}
