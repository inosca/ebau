import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";
import InquiryAnswerStatus from "ember-ebau-core/components/inquiry-answer-status";

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
  }
}
