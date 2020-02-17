import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class LogoutRoute extends Route {
  @service session;

  constructor(...args) {
    super(...args);
    this.session.invalidate();
  }
}
