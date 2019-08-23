import Route from "@ember/routing/route";
import OIDCApplicationRouteMixin from "ember-simple-auth-oidc/mixins/oidc-application-route-mixin";
import { inject as service } from "@ember/service";
import { getOwner } from "@ember/application";
import config from "../config/environment";

const { languages, fallbackLanguage } = config;

export default Route.extend(OIDCApplicationRouteMixin, {
  intl: service(),
  session: service(),
  calumaOptions: service(),

  getBrowserLanguage() {
    const preferred = (navigator.languages || [navigator.language]).map(
      locale => locale.split("-")[0]
    );

    return preferred.find(lang => languages.includes(lang));
  },

  getLocalStorageLanguage() {
    if (languages.includes(localStorage.getItem("language"))) {
      return localStorage.getItem("language");
    }
  },

  getLanguage(queryParamLanguage) {
    if (languages.includes(queryParamLanguage)) {
      return queryParamLanguage;
    }

    return (
      this.getLocalStorageLanguage() ||
      this.getBrowserLanguage() ||
      fallbackLanguage
    );
  },

  beforeModel(transition) {
    this.intl.setLocale([
      this.getLanguage(transition.to.queryParams.language),
      fallbackLanguage
    ]);

    if (window.top !== window) {
      getOwner(this)
        .lookup("service:-document")
        .querySelector("body")
        .classList.add("embedded");
    }

    this.calumaOptions.registerComponentOverride({
      label: "Karte",
      component: "be-gis"
    });
    this.calumaOptions.registerComponentOverride({
      label: "Einreichen Button",
      component: "be-submit-instance",
      type: "CheckboxQuestion"
    });
    this.calumaOptions.registerComponentOverride({
      label: "Dokument Formular",
      component: "be-documents-form",
      type: "FormQuestion"
    });
    this.calumaOptions.registerComponentOverride({
      label: "Download (PDF)",
      component: "be-download-pdf",
      type: "StaticQuestion"
    });
    this.calumaOptions.registerComponentOverride({
      label: "Nachforderungen Tabelle",
      component: "be-claims",
      type: "TableQuestion"
    });
  }
});
