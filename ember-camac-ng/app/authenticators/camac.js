import { assert } from "@ember/debug";
import { later, cancel } from "@ember/runloop";
import { inject as service } from "@ember/service";
import BaseAuthenticator from "ember-simple-auth/authenticators/base";
import fetch from "fetch";

export default class CamacAuthenticator extends BaseAuthenticator {
  @service shoebox;

  restore() {
    assert(
      "Token can't be restored since we don't have a persistent session store"
    );
  }

  async authenticate() {
    const token = this.shoebox.content.token;

    assert("No token data passed in shoebox", token);

    return this.handleToken(token);
  }

  async refresh() {
    const token = await fetch("/index/token", {
      credentials: "same-origin",
    }).then((response) => response.json());

    const data = this.handleToken(token);

    this.trigger("sessionDataUpdated", data);
  }

  handleToken(token) {
    const {
      expires_in: expiresIn,
      token_refresh_leeway: tokenRefreshLeeway,
    } = token;

    const timeout = expiresIn - tokenRefreshLeeway;

    if (timeout > 0) {
      cancel(this._timer);
      this._timer = later(this, "refresh", timeout * 1000);
    } else {
      this.refresh();
    }

    return token;
  }
}
