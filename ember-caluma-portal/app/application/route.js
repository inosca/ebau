import Route from "@ember/routing/route";
import OIDCApplicationRouteMixin from "ember-simple-auth-oidc/mixins/oidc-application-route-mixin";
import { inject as service } from "@ember/service";
import { getOwner } from "@ember/application";

const DEFAULT_LANG = "de";

export default Route.extend(OIDCApplicationRouteMixin, {
  intl: service(),
  calumaOptions: service(),

  chooseLanguage() {
    return localStorage.getItem("language") || DEFAULT_LANG;
  },

  beforeModel() {
    this.intl.setLocale([this.chooseLanguage()]);

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
