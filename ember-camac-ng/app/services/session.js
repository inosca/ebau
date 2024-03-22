import { inject as service } from "@ember/service";
import SessionService from "ember-simple-auth/services/session";

export default class CustomSessionService extends SessionService {
  @service shoebox;

  async getAuthorizationHeader() {
    if (
      this.isAuthenticated &&
      this.data.authenticated.refreshAt <= new Date()
    ) {
      const authenticator = this.session._lookupAuthenticator(
        "authenticator:camac",
      );

      await authenticator.refresh();
    }

    return `${this.data.authenticated.token_type} ${this.data.authenticated.access_token}`;
  }

  get isReadOnlyRole() {
    return this.shoebox.isReadOnlyRole;
  }

  get user() {
    return { id: this.shoebox.content.userId };
  }

  get authHeaders() {
    return {
      authorization: `${this.data.authenticated.token_type} ${this.data.authenticated.access_token}`,
      "x-camac-group": this.shoebox.content.groupId,
    };
  }

  get isInternal() {
    return Boolean(this.shoebox.content.groupId);
  }
}
