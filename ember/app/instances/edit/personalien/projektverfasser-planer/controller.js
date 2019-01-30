import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { computed } from "@ember/object";
import { mapBy } from "@ember/object/computed";

export default Controller.extend({
  questionStore: service("question-store"),

  fields: mapBy("model.instance.fields", "name"),

  questionActive: computed("model.instance.fields.@each", function() {
    return this.fields.includes("bauherrschaft");
  }),

  actions: {
    async copyQuestionValue() {
      let question = await this.questionStore.peek(
        "projektverfasser-planer",
        this.get("model.instance.id")
      );
      question.set("model.value", this.bauherrschaftValue);
      question.set("value", this.bauherrschaftValue);
      await this.get("questionStore.saveQuestion").perform(question);
    }
  }
});
