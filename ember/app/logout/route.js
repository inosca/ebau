import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";
import Ember from "ember";

export default class LogoutRoute extends Route {
  @service session;

  constructor(...args) {
    super(...args);

    if (!Ember.testing) {
      this.session.singleLogout();
    }
  }
}
