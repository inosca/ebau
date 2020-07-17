import Controller from "@ember/controller";
import { inject as service } from "@ember/service";

import config from "../config/environment";

const { environment, profileURL } = config;

export default Controller.extend({
  session: service(),

  environment,

  profileURL,

  isEmbedded: window !== window.top,
});
