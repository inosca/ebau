import { getOwner } from "@ember/application";
import { get } from "@ember/object";
import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";
import OIDCApplicationRouteMixin from "ember-simple-auth-oidc/mixins/oidc-application-route-mixin";

export default class ApplicationRoute extends Route.extend(
  OIDCApplicationRouteMixin
) {
  @service session;
  @service router;
  @service calumaOptions;

  queryParams = {
    language: { refreshModel: true },
    group: { refreshModel: true },
  };

  beforeModel(transition) {
    super.beforeModel(transition);

    const { language, group } = get(transition, "to.queryParams") || {};

    this.session.set("language", language || this.session.language);
    this.session.set("data.group", group || this.session.group);

    if (language || group) {
      // after the transition remove the query params so we don't persist the
      // language and group info twice (in the URL and in the session)
      transition.then(() => {
        this.replaceWith({ queryParams: { language: null, group: null } });
      });
    }

    if (window.top !== window) {
      getOwner(this)
        .lookup("service:-document")
        .querySelector("body")
        .classList.add("embedded");
    }

    this.calumaOptions.registerComponentOverride({
      label: "Karte",
      component: "be-gis",
    });
    this.calumaOptions.registerComponentOverride({
      label: "GIS-Karte (Kt. UR)",
      component: "ur-gis",
    });
    this.calumaOptions.registerComponentOverride({
      label: "Einreichen Button",
      component: "be-submit-instance",
      type: "CheckboxQuestion",
    });
    this.calumaOptions.registerComponentOverride({
      label: "Dokument Formular",
      component: "be-documents-form",
      type: "FormQuestion",
    });
    this.calumaOptions.registerComponentOverride({
      label: "Download (PDF)",
      component: "be-download-pdf",
      type: "StaticQuestion",
    });
    this.calumaOptions.registerComponentOverride({
      label: "Nachforderungen Formular",
      component: "be-claims-form",
      type: "Form",
    });
    this.calumaOptions.registerComponentOverride({
      label: "Versteckt",
      component: "cf-hidden-input",
    });
    this.calumaOptions.registerComponentOverride({
      label: "Deaktiviert",
      component: "be-disabled-input",
    });
    this.calumaOptions.registerComponentOverride({
      label: "eBau Nummer Vorschlagen",
      component: "suggest-ebau-number",
      type: "StaticQuestion",
    });
    this.calumaOptions.registerComponentOverride({
      label: "eBau Nummer Weiter Button",
      component: "assign-ebau-number-button",
      type: "StaticQuestion",
    });
  }
}
