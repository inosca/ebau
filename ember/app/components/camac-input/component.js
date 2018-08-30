import Component from "@ember/component";
import { inject as service } from "@ember/service";
import { computed } from "@ember/object";
import { task } from "ember-concurrency";

const CamacInputComponent = Component.extend({
  classNames: ["uk-margin"],

  identifier: null,

  instance: null,

  error: null,

  questionStore: service("question-store"),

  question: computed("identifier", function() {
    return this.questionStore.peek(this.identifier, this.instance.id);
  }),

  save: task(function*(value) {
    if (this.readonly) {
      return;
    }

    this.question.set("model.value", value);

    this.set(
      "error",
      yield this.get("questionStore.saveQuestion").perform(this.question)
    );
  }).restartable()
});

CamacInputComponent.reopenClass({
  positionalParams: ["identifier"]
});

export default CamacInputComponent;
