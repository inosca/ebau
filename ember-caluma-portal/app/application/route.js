import Route from "@ember/routing/route";
import OIDCApplicationRouteMixin from "ember-simple-auth-oidc/mixins/oidc-application-route-mixin";
import { inject as service } from "@ember/service";
import { getOwner } from "@ember/application";

const DEFAULT_LANG = "de";
const SUPPORTED_LANGUAGES = ["de", "fr"];

export default Route.extend(OIDCApplicationRouteMixin, {
  intl: service(),
  calumaOptions: service(),

  chooseLanguage() {
    const preferred = (navigator.languages || [navigator.language]).map(
      locale => locale.split("-")[0]
    );
    return (
      preferred.find(lang => SUPPORTED_LANGUAGES.includes(lang)) || DEFAULT_LANG
    );
  },

  beforeModel() {
    this.intl.setLocale([
      `${this.chooseLanguage()}-ch`,
      "de-de" // fallback language
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
  }
});
