import { getOwner } from "@ember/application";
import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";
import DocumentValidityButtonComponent from "ember-ebau-core/components/document-validity-button";
import LinkAttachmentsComponent from "ember-ebau-core/components/link-attachments";
import UrGisComponent from "ember-ebau-core/components/ur-gis";

import AssignEbauNumberButtonComponent from "camac-ng/components/assign-ebau-number-button";
import CfCollapsibleTextareaComponent from "camac-ng/components/cf-collapsible-textarea";
import CfDownloadPdfComponent from "camac-ng/components/cf-download-pdf";
import CfSnippetsTextComponent from "camac-ng/components/cf-snippets-text";
import CfSnippetsTextareaComponent from "camac-ng/components/cf-snippets-textarea";
import DecisionSubmitPartialComponent from "camac-ng/components/decision-submit-partial";
import InquiryAnswerStatus from "camac-ng/components/inquiry-answer-status";
import QrCodeComponent from "camac-ng/components/qr-code";
import SuggestEbauNumberComponent from "camac-ng/components/suggest-ebau-number";

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
      componentClass: UrGisComponent,
    });

    this.calumaOptions.registerComponentOverride({
      label: "Download (PDF)",
      component: "cf-download-pdf",
      componentClass: CfDownloadPdfComponent,
      type: "StaticQuestion",
    });

    this.calumaOptions.registerComponentOverride({
      label: "Collapsible Textarea",
      component: "cf-collapsible-textarea",
      componentClass: CfCollapsibleTextareaComponent,
      type: "TextareaQuestion",
    });

    this.calumaOptions.registerComponentOverride({
      label: "Text input with snippets",
      component: "cf-snippets-text",
      componentClass: CfSnippetsTextComponent,
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
      componentClass: QrCodeComponent,
      type: "StaticQuestion",
    });

    this.calumaOptions.registerComponentOverride({
      label: "eBau Nummer Vorschlagen",
      component: "suggest-ebau-number",
      componentClass: SuggestEbauNumberComponent,
      type: "StaticQuestion",
    });

    this.calumaOptions.registerComponentOverride({
      label: "eBau Nummer Weiter Button",
      component: "assign-ebau-number-button",
      componentClass: AssignEbauNumberButtonComponent,
      type: "StaticQuestion",
    });

    this.calumaOptions.registerComponentOverride({
      label: "Entscheid verfügen (Teilbaubewilligung)",
      component: "decision-submit-partial",
      componentClass: DecisionSubmitPartialComponent,
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

    this.calumaOptions.registerComponentOverride({
      label: "Dokumente verlinken",
      component: "link-attachments",
      componentClass: LinkAttachmentsComponent,
    });
  }
}
