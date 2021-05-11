import { assert } from "@ember/debug";
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

    return this.parseData(token);
  }

  async refresh() {
    try {
      const response = await fetch("/index/token", {
        credentials: "same-origin",
        mode: "same-origin",
        redirect: "error",
      });
      const data = await response.json();

      this.trigger("sessionDataUpdated", this.parseData(data));
    } catch (error) {
      location.reload();
    }
  }

  parseData(raw) {
    return {
      ...raw,
      refreshAt: new Date(
        new Date().getTime() +
          (raw.expires_in - raw.token_refresh_leeway) * 1000
      ),
    };
  }
}
