import Route from "@ember/routing/route";
import { service } from "@ember/service";
import CamacAdditionalDemandFilesComponent from "ember-ebau-core/components/camac-additional-demand-files";
import DecisionAppealButtonComponent from "ember-ebau-core/components/decision/appeal-button";
import DecisionInfoAppealComponent from "ember-ebau-core/components/decision/info-appeal";
import DecisionInfoGeometerComponent from "ember-ebau-core/components/decision/info-geometer";
import DecisionInfoMissingGeometerInvolvementComponent from "ember-ebau-core/components/decision/info-missing-geometer-involvement";
import DecisionSubmitButtonComponent from "ember-ebau-core/components/decision/submit-button";
import DocumentValidityButtonComponent from "ember-ebau-core/components/document-validity-button";
import InquiryAnswerStatus from "ember-ebau-core/components/inquiry-answer-status";
import InquiryDeadlineInputComponent from "ember-ebau-core/components/inquiry-deadline-input";
import LinkAttachmentsComponent from "ember-ebau-core/components/link-attachments";
import MilestoneValuesComponent from "ember-ebau-core/components/milestone-values";
import UrGisComponent from "ember-ebau-core/components/ur-gis";
import mainConfig from "ember-ebau-core/config/main";
import UIkit from "uikit";

import AssignEbauNumberButtonComponent from "camac-ng/components/assign-ebau-number-button";
import CfCollapsibleTextareaComponent from "camac-ng/components/cf-collapsible-textarea";
import CfDownloadPdfComponent from "camac-ng/components/cf-download-pdf";
import CfSnippetsTextComponent from "camac-ng/components/cf-snippets-text";
import CfSnippetsTextareaComponent from "camac-ng/components/cf-snippets-textarea";
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
      const application = mainConfig.name;

      this.intl.setLocale([
        `${language}-ch`,
        `${language}-${application}`,
        language,
      ]);

      UIkit.modal.i18n = {
        ok: this.intl.t("global.ok"),
        cancel: this.intl.t("global.cancel"),
      };
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

    this.calumaOptions.registerComponentOverride({
      label: "Hilfetext Beschwerdeverfahren",
      component: "decision/info-appeal",
      componentClass: DecisionInfoAppealComponent,
    });

    this.calumaOptions.registerComponentOverride({
      label: "Hilfetext Nachführungsgeometer",
      component: "decision/info-geometer",
      componentClass: DecisionInfoGeometerComponent,
    });

    this.calumaOptions.registerComponentOverride({
      label: "Hilfetext fehlende Einbindung des Nachführungsgeometer",
      component: "decision/info-missing-geometer-involvement",
      componentClass: DecisionInfoMissingGeometerInvolvementComponent,
    });

    this.calumaOptions.registerComponentOverride({
      label: "Entscheid verfügen",
      component: "decision/submit-button",
      componentClass: DecisionSubmitButtonComponent,
    });

    this.calumaOptions.registerComponentOverride({
      label: "Beschwerde eingegangen",
      component: "decision/appeal-button",
      componentClass: DecisionAppealButtonComponent,
    });

    this.calumaOptions.registerComponentOverride({
      label: "Stellungnahme deadline",
      component: "inquiry-deadline-input",
      componentClass: InquiryDeadlineInputComponent,
    });

    this.calumaOptions.registerComponentOverride({
      label: "Milestone values (Kt. UR)",
      component: "milestone-values",
      componentClass: MilestoneValuesComponent,
    });

    this.calumaOptions.registerComponentOverride({
      label: "Nachforderungsdateien Camac (Kt. UR)",
      component: "camac-additional-demand-files",
      componentClass: CamacAdditionalDemandFilesComponent,
    });
  }
}
