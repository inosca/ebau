import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";
import CalculatedPublicationDateComponent from "ember-ebau-core/components/calculated-publication-date";
import InquiryAnswerStatus from "ember-ebau-core/components/inquiry-answer-status";
import PublicationDateKantonsamtsblattComponent from "ember-ebau-core/components/publication-date-kantonsamtsblatt";

export default class ApplicationRoute extends Route {
  @service session;
  @service calumaOptions;

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
  }
}
