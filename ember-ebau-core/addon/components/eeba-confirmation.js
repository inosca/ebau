import { service } from "@ember/service";
import Component from "@glimmer/component";
import { task } from "ember-concurrency";

import { EEBA_ANSWER_QUESTIONS, EEBA_STATE } from "ember-ebau-core/config/eeba";
export default class EebaConfirmationComponent extends Component {
  @service eebaClient;
  @service session;
  @service fetch;
  @service ebauModules;

  get instanceId() {
    return this.args.context.instanceId;
  }

  get eebaStateAnswer() {
    return this.getAnswer(EEBA_ANSWER_QUESTIONS.STATE) || EEBA_STATE.NONE;
  }

  get hasEebaRequiredAnswer() {
    return this.getAnswer(EEBA_ANSWER_QUESTIONS.REQUIRED) !== null;
  }

  get eebaRequiredAnswer() {
    return (
      this.getAnswer(EEBA_ANSWER_QUESTIONS.REQUIRED) ===
      `${EEBA_ANSWER_QUESTIONS.REQUIRED}-ja`
    );
  }

  get eebaIntegrationIdAnswer() {
    return this.getAnswer(EEBA_ANSWER_QUESTIONS.INTEGRATION_ID);
  }

  get hasExistingEeba() {
    return (
      this.getAnswer(
        "haben-sie-bereits-eeba-direkt-auf-eeba-onlineservice-erfasst",
      ) ===
      "haben-sie-bereits-eeba-direkt-auf-dem-eeba-onlineservice-erfasst-ja"
    );
  }

  get eebaWebUrlAnswer() {
    return this.getAnswer(EEBA_ANSWER_QUESTIONS.WEB_URL);
  }

  get eebaIsDirtyAnswer() {
    return (
      this.getAnswer(EEBA_ANSWER_QUESTIONS.IS_DIRTY) ===
      `${EEBA_ANSWER_QUESTIONS.IS_DIRTY}-ja`
    );
  }

  get eebaStateClass() {
    switch (this.eebaStateAnswer) {
      case EEBA_STATE.NONE:
        return "uk-text-muted";
      case EEBA_STATE.COMPLETED:
        return "uk-text-success";
      default:
        return "uk-text-warning";
    }
  }

  get canCheckIntegration() {
    return (
      !this.session.isInternal &&
      (this.eebaIsDirtyAnswer ||
        [EEBA_STATE.NONE, EEBA_STATE.RERUN, EEBA_STATE.RETRY].includes(
          this.eebaStateAnswer,
        ))
    );
  }

  get showRecheck() {
    return this.eebaIsDirtyAnswer && this.eebaStateAnswer !== EEBA_STATE.RERUN;
  }

  getAnswer(slug) {
    try {
      return this.args.field.document.findField(slug)?.answer?.value;
    } catch (error) {
      console.error(`Error retrieving answer for slug "${slug}":`, error);
      return null;
    }
  }

  checkIntegration = task({ restartable: true }, async () => {
    if (!this.canCheckIntegration) {
      return;
    }

    try {
      const result = await this.eebaClient.checkIntegration(
        this.instanceId,
        {},
      );
      const isDirtyField = this.args.field.document.findField(
        EEBA_ANSWER_QUESTIONS.IS_DIRTY,
      );
      isDirtyField.answer.value = `${EEBA_ANSWER_QUESTIONS.IS_DIRTY}-nein`;
      // saving the dirty field will also trigger the refresh of all linked fields.
      await isDirtyField.save.perform();

      return result;
    } catch {
      this.eebaClient.onSaveEebaRefresh(
        this.args.field.document,
        this.args.field.document.findField(EEBA_ANSWER_QUESTIONS.CONFIRMATION)
          .question.raw,
      );
    }
  });
}
