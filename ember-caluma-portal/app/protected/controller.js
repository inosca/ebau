import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import config from "../config/environment";

const { environment } = config;

export default Controller.extend({
  init() {
    this._super(...arguments);

    this.languages = ["de", "fr"];
  },
  intl: service(),
  session: service(),
  environment,
  actions: {
    setLanguage(language) {
      localStorage.setItem("language", language);
      this.intl.setLocale(localStorage.getItem("lagnuage"));
      window.location.reload(true);
    }
  }
});
