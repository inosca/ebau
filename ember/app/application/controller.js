import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import config from "../config/environment";

const { environment, oidcHost } = config;

export default Controller.extend({
  session: service(),

  environment,

  oidcHost,

  isEmbedded: window !== window.top,

  actions: {
    logout() {
      this.session.invalidate();
    }
  }
});
