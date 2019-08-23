import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import config from "../config/environment";
import { computed } from "@ember/object";

const { environment, languages, fallbackLanguage } = config;

export default Controller.extend({
  intl: service(),
  session: service(),

  languages,
  environment,

  enableMultilang: computed(() => {
    // TODO: remove this if the french translations are approved
    return !/ebau.apps.be.ch$/.test(window.location.host);
  }),

  actions: {
    setLanguage(language) {
      if (!this.enableMultilang) return;

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
