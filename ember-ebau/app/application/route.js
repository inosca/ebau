import Route from "@ember/routing/route";
import { service } from "@ember/service";
import AdditionalDemandAllowChangesComponent from "ember-ebau-core/components/additional-demand-allow-changes";
import AdditionalDemandFormTimelineLinkComponent from "ember-ebau-core/components/additional-demand-formtimeline-link";
import AgGisComponent from "ember-ebau-core/components/ag-gis";
import AGInquiryServiceGroupWarningComponent from "ember-ebau-core/components/ag-inquiry-service-group-warning";
import AlexandriaDocumentsFormComponent from "ember-ebau-core/components/alexandria-documents-form";
import ApplicantConfirmationsWidgetComponent from "ember-ebau-core/components/applicant-confirmations/widget";
import CalculatedPublicationDateComponent from "ember-ebau-core/components/calculated-publication-date";
import CfSnippetsTextareaComponent from "ember-ebau-core/components/cf-snippets-textarea";
import CheckHintNewAddressNeededComponent from "ember-ebau-core/components/check-hint-new-address-needed";
import ConstructionMonitoringGeometerChoiceComponent from "ember-ebau-core/components/construction-monitoring-geometer-choice";
import CoordinatesPlaceholderComponent from "ember-ebau-core/components/coordinates-placeholder";
import DecisionAppealButtonComponent from "ember-ebau-core/components/decision/appeal-button";
import DecisionInfoAppealComponent from "ember-ebau-core/components/decision/info-appeal";
import DecisionSubmitButtonComponent from "ember-ebau-core/components/decision/submit-button";
import DirectInquiryCheckboxComponent from "ember-ebau-core/components/direct-inquiry-checkbox";
import DynamicMaxDateInputComponent from "ember-ebau-core/components/dynamic-max-date-input";
import EebaConfirmationComponent from "ember-ebau-core/components/eeba-confirmation";
import EebaLinkComponent from "ember-ebau-core/components/eeba-link";
import ExamResultTextareaComponent from "ember-ebau-core/components/exam-result-textarea";
import GrGisComponent from "ember-ebau-core/components/gr-gis";
import InquiryAnswerStatus from "ember-ebau-core/components/inquiry-answer-status";
import InquiryDeadlineInputComponent from "ember-ebau-core/components/inquiry-deadline-input";
import InquiryHintDeadlineExpiredComponent from "ember-ebau-core/components/inquiry-hint-deadline-expired";
import InquiryHintOpenSuspensionsComponent from "ember-ebau-core/components/inquiry-hint-open-suspensions";
import KeycloakProfileApplyButtonComponent from "ember-ebau-core/components/keycloak-profile-apply-button";
import PublicationDateKantonsamtsblattComponent from "ember-ebau-core/components/publication-date-kantonsamtsblatt";
import PublicationFillEndDateComponent from "ember-ebau-core/components/publication-fill-end-date";
import PublicationStartDateComponent from "ember-ebau-core/components/publication-start-date";
import QrCodeComponent from "ember-ebau-core/components/qr-code";
import SgGisComponent from "ember-ebau-core/components/sg-gis";
import ShowIfInquiryQuestionHasValue from "ember-ebau-core/components/show-if-inquiry-question-has-value";
import SoGisComponent from "ember-ebau-core/components/so-gis";
import SubmitInstanceComponent from "ember-ebau-core/components/submit-instance";

export default class ApplicationRoute extends Route {
  @service session;
  @service calumaOptions;
  @service router;

  async beforeModel(transition) {
    super.beforeModel(transition);

    await this.session.setup();

    // trigger the setter to initialize i18n
    // TODO: the initialization might be better placed in the session setup hook
    // eslint-disable-next-line no-self-assign
    this.session.language = this.session.language;

    // component overrides.
    this.calumaOptions.registerComponentOverride({
      label: "Stellungnahme Status",
      component: "inquiry-answer-status",
      componentClass: InquiryAnswerStatus,
      type: "ChoiceQuestion",
    });
    this.calumaOptions.registerComponentOverride({
      label: "Berechnetes Publikations-Enddatum",
      component: "calculated-publication-date",
      componentClass: CalculatedPublicationDateComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "Publikationsbeginn Kanton",
      component: "publication-date-kantonsamtsblatt",
      componentClass: PublicationDateKantonsamtsblattComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "GIS-Karte (Kt. SO)",
      component: "so-gis",
      componentClass: SoGisComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "GIS-Karte (Kt. GR)",
      component: "gr-gis",
      componentClass: GrGisComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "GIS-Karte (Kt. AG)",
      component: "ag-gis",
      componentClass: AgGisComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "GIS-Karte (Kt. SG)",
      component: "sg-gis",
      componentClass: SgGisComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "Eeba Link",
      component: "eeba-link",
      componentClass: EebaLinkComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "Eeba Bestätigung",
      component: "eeba-confirmation",
      componentClass: EebaConfirmationComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "Alexandria Dokument Formular",
      component: "alexandria-documents-form",
      componentClass: AlexandriaDocumentsFormComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "Datum Anzeiger und Datum Amtsblatt (Kt. SO)",
      component: "dynamic-max-date-input",
      componentClass: DynamicMaxDateInputComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "Start Auflage (Kt. SO)",
      component: "publication-start-date",
      componentClass: PublicationStartDateComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "Stellungnahme Frist",
      component: "inquiry-deadline-input",
      componentClass: InquiryDeadlineInputComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "Keycloak Profil anwenden",
      component: "keycloak-profile-apply-button",
      componentClass: KeycloakProfileApplyButtonComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "Beschwerde eingegangen",
      component: "decision/appeal-button",
      componentClass: DecisionAppealButtonComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "Hilfetext Beschwerdeverfahren",
      component: "decision/info-appeal",
      componentClass: DecisionInfoAppealComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "Entscheid verfügen",
      component: "decision/submit-button",
      componentClass: DecisionSubmitButtonComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "Einreichen Button",
      component: "submit-instance",
      componentClass: SubmitInstanceComponent,
      type: "CheckboxQuestion",
    });
    this.calumaOptions.registerComponentOverride({
      label: "Koordinaten Platzhalter",
      component: "coordinates-placeholder",
      componentClass: CoordinatesPlaceholderComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "Textfeld Prüfungsergebnis",
      component: "exam-result-textarea",
      componentClass: ExamResultTextareaComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "Checkbox direkte Erledigung",
      component: "direct-inquiry-checkbox",
      componentClass: DirectInquiryCheckboxComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label:
        "Frage anzeigen wenn konfigurierte Stellungnahme-Frage konfiguriertem Wert entspricht",
      component: "show-if-inquiry-question-has-value",
      componentClass: ShowIfInquiryQuestionHasValue,
    });
    this.calumaOptions.registerComponentOverride({
      label: "AG: Zirkulation Warnung Organisationstyp",
      component: "ag-inquiry-service-group-warning",
      componentClass: AGInquiryServiceGroupWarningComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "Publikation Startdatum mit automatischem Ausfüllen des Enddatums",
      component: "publication-fill-end-date",
      componentClass: PublicationFillEndDateComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "QR Code",
      component: "qr-code",
      componentClass: QrCodeComponent,
      type: "StaticQuestion",
    });
    this.calumaOptions.registerComponentOverride({
      label: "Hinweis Zirkulation bei offenen Sistierungen",
      component: "inquiry-hint-open-suspensions",
      componentClass: InquiryHintOpenSuspensionsComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "Hinweis Zirkulation bei abgelaufener Frist",
      component: "inquiry-hint-deadline-expired",
      componentClass: InquiryHintDeadlineExpiredComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "Nachforderung Anpassungen erlauben",
      component: "additional-demand-allow-changes",
      componentClass: AdditionalDemandAllowChangesComponent,
      type: "MultipleChoiceQuestion",
    });
    this.calumaOptions.registerComponentOverride({
      label: "Nachforderung Anpassungen Link",
      component: "additional-demand-formtimeline-link",
      componentClass: AdditionalDemandFormTimelineLinkComponent,
      type: "TextQuestion",
    });
    this.calumaOptions.registerComponentOverride({
      label: "Hinweis neue Adresse notwendig",
      component: "check-hint-new-address-needed",
      componentClass: CheckHintNewAddressNeededComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "Baubegleitung Geometer Auswahl",
      component: "construction-monitoring-geometer-choice",
      componentClass: ConstructionMonitoringGeometerChoiceComponent,
      type: "ChoiceQuestion",
    });
    this.calumaOptions.registerComponentOverride({
      label: "Textarea with snippets",
      component: "cf-snippets-textarea",
      componentClass: CfSnippetsTextareaComponent,
      type: "TextareaQuestion",
    });
    this.calumaOptions.registerComponentOverride({
      label: "Bestätigung Gesuchsteller",
      component: "applicant-confirmations/widget",
      componentClass: ApplicantConfirmationsWidgetComponent,
      type: "MultipleChoiceQuestion",
    });
  }
}
