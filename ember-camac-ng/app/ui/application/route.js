import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class ApplicationRoute extends Route {
  @service intl;
  @service session;
  @service shoebox;
  @service moment;
  @service calumaOptions;

  async beforeModel(transition) {
    await this.session.setup();

    this.session.requireAuthentication(transition, () => {
      this.session.authenticate("authenticator:camac");
    });

    const language = this.shoebox.content.language;

    if (language) {
      const locale = `${language}-ch`;

      this.intl.setLocale([locale, language]);
      this.moment.setLocale(locale);
    }

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
