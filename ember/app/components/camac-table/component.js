import { action, computed, set } from "@ember/object";
import { inject as service } from "@ember/service";
import CamacInputComponent from "citizen-portal/components/camac-input/component";
import CamacMultipleQuestionMixin from "citizen-portal/mixins/camac-multiple-question";

export default class CamacTableComponent extends CamacInputComponent.extend(
  CamacMultipleQuestionMixin
) {
  showModal = false;
  copySourceValue;
  model;
  copySource = null;

  @service("question-store") questionStore;
  @service notification;

  async init(...args) {
    super.init(...args);

    if (this.copySource) {
      const question = await this.questionStore.peek(
        this.copySource,
        this.model.instance.id
      );

      set(this, "copySourceValue", question.value ?? []);

      // trigger validation errors for incorrect table answer copies
      const tableQuestion = await this.questionStore.peek(
        this.identifier,
        this.model.instance.id
      );

      if (tableQuestion.model?.value?.length) {
        const validity = tableQuestion.validate();
        if (validity !== true) {
          set(this, "error", validity);
        }
      }
    }
  }

  @computed("model.instance.fields.@each")
  get questionActive() {
    return (
      this.model &&
      this.model.meta.editable.includes("form") &&
      this.model.instance.fields.findBy("name", this.copySource)
    );
  }

  @action
  async copyQuestionValue() {
    const question = await this.questionStore.peek(
      this.identifier,
      this.model.instance.id
    );
    set(
      question,
      "model.value",
      (this.model.value ?? []).pushObjects(this.copySourceValue).uniqBy("uuid")
    );

    set(this, "error", await this.questionStore.saveQuestion.perform(question));
    // ignore validation errors while copying, still
    // indicated in navigation tree and below table
    if (this.error) {
      question.model.save();
    }
  }
}
