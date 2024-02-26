import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";
import AlexandriaDocumentsFormComponent from "ember-ebau-core/components/alexandria-documents-form";
import CalculatedPublicationDateComponent from "ember-ebau-core/components/calculated-publication-date";
import DecisionAppealButtonComponent from "ember-ebau-core/components/decision/appeal-button";
import DecisionInfoAppealComponent from "ember-ebau-core/components/decision/info-appeal";
import DecisionSubmitButtonComponent from "ember-ebau-core/components/decision/submit-button";
import DynamicMaxDateInputComponent from "ember-ebau-core/components/dynamic-max-date-input";
import GrGisComponent from "ember-ebau-core/components/gr-gis";
import InquiryAnswerStatus from "ember-ebau-core/components/inquiry-answer-status";
import InquiryDeadlineInputComponent from "ember-ebau-core/components/inquiry-deadline-input";
import PublicationDateKantonsamtsblattComponent from "ember-ebau-core/components/publication-date-kantonsamtsblatt";
import PublicationStartDateComponent from "ember-ebau-core/components/publication-start-date";
import SoGisComponent from "ember-ebau-core/components/so-gis";

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
      label: "GIS-Karte (Kt. GR)",
      component: "gr-gis",
      componentClass: GrGisComponent,
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
  }
}
