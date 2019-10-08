import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import config from "../config/environment";

const { environment, languages, fallbackLanguage } = config;

export default Controller.extend({
  intl: service(),
  session: service(),

  languages,
  environment,

  actions: {
    setLanguage(language) {
      if (languages.includes(language)) {
        localStorage.setItem("language", language);

        this.intl.setLocale([
          localStorage.getItem("language"),
          fallbackLanguage
        ]);

        window.location.reload(true);
      }
    }
  }
});
