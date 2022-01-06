import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";
import ApplicationRouteMixin from "ember-simple-auth/mixins/application-route-mixin";
import AuthenticatedRouteMixin from "ember-simple-auth/mixins/authenticated-route-mixin";
import moment from "moment";

const ApplicationRouteBase = Route.extend(
  ApplicationRouteMixin,
  AuthenticatedRouteMixin
);

export default class ApplicationRoute extends ApplicationRouteBase {
  @service intl;
  @service session;
  @service shoebox;
  @service calumaOptions;

  async beforeModel(...args) {
    super.beforeModel(...args);

    this.intl.setLocale(this.shoebox.content.language);
    moment.locale(this.shoebox.content.language);

    this.calumaOptions.registerComponentOverride({
      label: "Karte",
      component: "ur-gis",
    });

    this.calumaOptions.registerComponentOverride({
      label: "Download (PDF)",
      component: "cf-download-pdf",
      type: "StaticQuestion",
    });

    this.calumaOptions.registerComponentOverride({
      label: "Versteckt",
      component: "cf-hidden-input",
    });

    this.calumaOptions.registerComponentOverride({
      label: "Collapsible Textarea",
      component: "cf-collapsible-textarea",
      type: "TextareaQuestion",
    });

    this.calumaOptions.registerComponentOverride({
      label: "Text input with textcomponents",
      component: "cf-text-textcomponent",
      type: "TextQuestion",
    });

    this.calumaOptions.registerComponentOverride({
      label: "Textarea with textcomponents",
      component: "cf-textarea-textcomponent",
      type: "TextareaQuestion",
    });

    this.calumaOptions.registerComponentOverride({
      label: "QR Code",
      component: "qr-code",
      type: "StaticQuestion",
    });

    this.calumaOptions.registerComponentOverride({
      label: "Task form button",
      component: "task-form-button",
      type: "StaticQuestion",
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

  sessionInvalidated() {
    this.session.authenticate("authenticator:camac");
  }

  triggerAuthentication() {
    return this.session.authenticate("authenticator:camac");
  }
}
