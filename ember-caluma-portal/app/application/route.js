import { getOwner } from "@ember/application";
import Route from "@ember/routing/route";
import { service } from "@ember/service";
import AgGisComponent from "ember-ebau-core/components/ag-gis";
import AlexandriaDocumentsFormComponent from "ember-ebau-core/components/alexandria-documents-form";
import CalculatedPublicationDateComponent from "ember-ebau-core/components/calculated-publication-date";
import CamacAdditionalDemandFilesComponent from "ember-ebau-core/components/camac-additional-demand-files";
import CoordinatesPlaceholderComponent from "ember-ebau-core/components/coordinates-placeholder";
import DecisionAppealButtonComponent from "ember-ebau-core/components/decision/appeal-button";
import DecisionInfoAppealComponent from "ember-ebau-core/components/decision/info-appeal";
import DecisionInfoGeometerComponent from "ember-ebau-core/components/decision/info-geometer";
import DecisionInfoMissingGeometerInvolvementComponent from "ember-ebau-core/components/decision/info-missing-geometer-involvement";
import DecisionSubmitButtonComponent from "ember-ebau-core/components/decision/submit-button";
import DirectInquiryCheckboxComponent from "ember-ebau-core/components/direct-inquiry-checkbox";
import DirectInquiryInfoComponent from "ember-ebau-core/components/direct-inquiry-info";
import DocumentValidityButtonComponent from "ember-ebau-core/components/document-validity-button";
import DynamicMaxDateInputComponent from "ember-ebau-core/components/dynamic-max-date-input";
import ExamResultTextareaComponent from "ember-ebau-core/components/exam-result-textarea";
import GrGisComponent from "ember-ebau-core/components/gr-gis";
import InquiryAnswerStatus from "ember-ebau-core/components/inquiry-answer-status";
import InquiryDeadlineInputComponent from "ember-ebau-core/components/inquiry-deadline-input";
import KeycloakProfileApplyButtonComponent from "ember-ebau-core/components/keycloak-profile-apply-button";
import LinkAttachmentsComponent from "ember-ebau-core/components/link-attachments";
import PublicationDateKantonsamtsblattComponent from "ember-ebau-core/components/publication-date-kantonsamtsblatt";
import PublicationStartDateComponent from "ember-ebau-core/components/publication-start-date";
import ServiceContentComponent from "ember-ebau-core/components/service-content";
import SoGisComponent from "ember-ebau-core/components/so-gis";
import UrGisComponent from "ember-ebau-core/components/ur-gis";

import BeClaimsFormComponent from "caluma-portal/components/be-claims-form";
import BeDisabledInputComponent from "caluma-portal/components/be-disabled-input";
import BeDocumentsFormComponent from "caluma-portal/components/be-documents-form";
import BeDownloadPdfComponent from "caluma-portal/components/be-download-pdf";
import BeGisComponent from "caluma-portal/components/be-gis";
import BeSubmitInstanceComponent from "caluma-portal/components/be-submit-instance";
import GRSubmitInstanceComponent from "caluma-portal/components/gr-submit-instance";
import { isEmbedded } from "caluma-portal/helpers/is-embedded";

export default class ApplicationRoute extends Route {
  @service session;
  @service router;
  @service calumaOptions;

  queryParams = {
    language: { refreshModel: true },
    group: { refreshModel: true },
    referrer: { refreshModel: true },
  };

  async beforeModel(transition) {
    super.beforeModel(transition);

    await this.session.setup();

    const {
      language,
      group: groupId,
      referrer,
    } = transition.to?.queryParams ?? {};

    this.session.language = language ?? this.session.language;
    this.session.groupId = groupId ?? this.session.groupId;

    if (referrer) {
      this.session.set("data.referrer", referrer);
    }

    if (language || groupId || referrer) {
      // after the transition remove the query params so we don't persist the
      // language and group info twice (in the URL and in the session)
      transition.then(() => {
        this.router.replaceWith({
          queryParams: { language: null, group: null, referrer: null },
        });
      });
    }

    if (isEmbedded()) {
      getOwner(this)
        .lookup("service:-document")
        .querySelector("body")
        .classList.add("embedded");
    }

    this.calumaOptions.registerComponentOverride({
      label: "Karte",
      component: "be-gis",
      componentClass: BeGisComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "GIS-Karte (Kt. UR)",
      component: "ur-gis",
      componentClass: UrGisComponent,
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
      label: "Einreichen Button BE",
      component: "be-submit-instance",
      componentClass: BeSubmitInstanceComponent,
      type: "CheckboxQuestion",
    });
    this.calumaOptions.registerComponentOverride({
      label: "Einreichen Button GR",
      component: "gr-submit-instance",
      componentClass: GRSubmitInstanceComponent,
      type: "CheckboxQuestion",
    });
    this.calumaOptions.registerComponentOverride({
      label: "Dokument Formular",
      component: "be-documents-form",
      componentClass: BeDocumentsFormComponent,
      type: "FormQuestion",
    });
    this.calumaOptions.registerComponentOverride({
      label: "Download (PDF)",
      component: "be-download-pdf",
      componentClass: BeDownloadPdfComponent,
      type: "StaticQuestion",
    });
    this.calumaOptions.registerComponentOverride({
      label: "Nachforderungen Formular",
      component: "be-claims-form",
      componentClass: BeClaimsFormComponent,
      type: "Form",
    });
    this.calumaOptions.registerComponentOverride({
      label: "Deaktiviert",
      component: "be-disabled-input",
      componentClass: BeDisabledInputComponent,
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
      label: "Validierungs Button",
      component: "document-validity-button",
      componentClass: DocumentValidityButtonComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "Dokumente verlinken",
      component: "link-attachments",
      componentClass: LinkAttachmentsComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "Alexandria Dokument Formular",
      component: "alexandria-documents-form",
      componentClass: AlexandriaDocumentsFormComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "Stellungnahme Status",
      component: "inquiry-answer-status",
      componentClass: InquiryAnswerStatus,
      type: "ChoiceQuestion",
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
      label: "Berechnetes Publikations-Enddatum",
      component: "calculated-publication-date",
      componentClass: CalculatedPublicationDateComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "Publikationsbeginn Kanton (jeweils Donnerstag)",
      component: "publication-date-kantonsamtsblatt",
      componentClass: PublicationDateKantonsamtsblattComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "GIS-Karte (Kt. SO)",
      component: "so-gis",
      componentClass: SoGisComponent,
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
      label: "Koordinaten Platzhalter",
      component: "coordinates-placeholder",
      componentClass: CoordinatesPlaceholderComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "Keycloak Profil anwenden",
      component: "keycloak-profile-apply-button",
      componentClass: KeycloakProfileApplyButtonComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "Gemeindespezifischer Inhalt",
      component: "service-content",
      componentClass: ServiceContentComponent,
      type: "StaticQuestion",
    });
    this.calumaOptions.registerComponentOverride({
      label: "Nachforderungsdateien Camac (Kt. UR)",
      component: "camac-additional-demand-files",
      componentClass: CamacAdditionalDemandFilesComponent,
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
      label: "Infotext direkte Erledigung",
      component: "direct-inquiry-info",
      componentClass: DirectInquiryInfoComponent,
    });
  }
}
