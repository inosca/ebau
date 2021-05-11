import SessionService from "ember-simple-auth/services/session";

export default class CustomSessionService extends SessionService {
  async getAuthorizationHeader() {
    if (
      this.isAuthenticated &&
      this.data.authenticated.refreshAt <= new Date()
    ) {
      const authenticator = this.session._lookupAuthenticator(
        "authenticator:camac"
      );

      await authenticator.refresh();
    }

    return `${this.data.authenticated.token_type} ${this.data.authenticated.access_token}`;
  }
}
