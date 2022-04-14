import { getOwner } from "@ember/application";
import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";
import DocumentValidityButtonComponent from "ember-ebau-core/components/document-validity-button";

import CfSnippetsTextareaComponent from "camac-ng/ui/components/cf-snippets-textarea/component";
import InquiryAnswerStatus from "camac-ng/ui/components/inquiry-answer-status/component";

export default class ApplicationRoute extends Route {
  @service intl;
  @service session;
  @service shoebox;
  @service calumaOptions;

  async beforeModel(transition) {
    await this.session.setup();

    this.session.requireAuthentication(transition, () => {
      this.session.authenticate("authenticator:camac");
    });

    const language = this.shoebox.content.language;

    if (language) {
      const application =
        getOwner(this).resolveRegistration("config:environment").APPLICATION
          .name;

      this.intl.setLocale([
        `${language}-ch`,
        `${language}-${application}`,
        language,
      ]);
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
      label: "Collapsible Textarea",
      component: "cf-collapsible-textarea",
      type: "TextareaQuestion",
    });

    this.calumaOptions.registerComponentOverride({
      label: "Text input with snippets",
      component: "cf-snippets-text",
      type: "TextQuestion",
    });

    this.calumaOptions.registerComponentOverride({
      label: "Textarea with snippets",
      component: "cf-snippets-textarea",
      componentClass: CfSnippetsTextareaComponent,
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

    this.calumaOptions.registerComponentOverride({
      label: "Entscheid verfügen (Teilbaubewilligung)",
      component: "decision-submit-partial",
      type: "StaticQuestion",
    });

    this.calumaOptions.registerComponentOverride({
      label: "Validierungs Button",
      component: "document-validity-button",
      componentClass: DocumentValidityButtonComponent,
    });

    this.calumaOptions.registerComponentOverride({
      label: "Stellungnahme Status",
      component: "inquiry-answer-status",
      componentClass: InquiryAnswerStatus,
      type: "ChoiceQuestion",
    });
  }
}
