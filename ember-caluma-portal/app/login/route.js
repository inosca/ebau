import { getConfig } from "@embroider/macros";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";
import OIDCAuthenticationRoute from "ember-simple-auth-oidc/routes/oidc-authentication";
import { fetch } from "fetch";

function getQueryParam(transition, name) {
  const queryParams = transition.to
    ? transition.to.queryParams
    : transition.queryParams;

  return queryParams?.[name];
}

export default class LoginRoute extends OIDCAuthenticationRoute {
  queryParams = {
    token: { refreshModel: true },
  };

  async afterModel(_, transition) {
    const referrer = this.session.data.referrer;

    if (
      !hasFeature("login.tokenExchange") ||
      referrer === "internal" ||
      getQueryParam(transition, "code")
    ) {
      // If token exchange is disabled or the referrer comes from ember-ebau
      // (internal) we use the regular OIDC authentication
      if (referrer) {
        this.session.set("data.referrer", undefined);
      }
      return await super.afterModel(_, transition);
    }

    return await this.handleTokenExchangeAuthentication(transition);
  }

  async handleTokenExchangeAuthentication(transition) {
    const token = getQueryParam(transition, "token");

    if (token) {
      // If we have a token from the eGov portal, we need to exchange it for a
      // token from our OIDC provider
      return await this.exchangeToken(token);
    }

    if (!this.session.data.nextURL) {
      const url = this.session.attemptedTransition?.intent?.url;
      this.session.set("data.nextURL", url);
    }

    location.replace(
      [
        getConfig("ember-ebau-core").eGovPortalURL,
        getConfig("ember-ebau-core").eGovPrestationPath,
        `?redirectUrl=${this.redirectUri}`,
      ].join(""),
    );
  }

  async exchangeToken(token) {
    try {
      const response = await fetch("/api/v1/auth/token-exchange", {
        method: "POST",
        body: JSON.stringify({ "jwt-token": token }),
        headers: {
          accept: "application/json",
          "content-type": "application/json",
        },
      });

      if (!response.ok) {
        const { detail } = await response.json();
        throw new Error(detail);
      }

      // initialize session with already existing token
      // this is unusual for OIDC, so we need to call a private method
      this.session.session._setup(
        "authenticator:oidc",
        await response.json(),
        true,
      );
    } catch (error) {
      console.error(error);
    }
  }
}
