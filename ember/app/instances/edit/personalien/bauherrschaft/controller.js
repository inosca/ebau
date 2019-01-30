import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { computed } from "@ember/object";
import { mapBy } from "@ember/object/computed";

export default Controller.extend({
  questionStore: service("question-store"),

  fields: mapBy("model.instance.fields", "name"),

  questionActive: computed("model.instance.fields.@each", function() {
    return this.fields.includes("grundeigentumerschaft");
  }),

  actions: {
    async copyQuestionValue() {
      let question = await this.questionStore.peek(
        "bauherrschaft",
        this.get("model.instance.id")
      );
      question.set("model.value", this.grundeigentumerschaftValue);
      question.set("value", this.grundeigentumerschaftValue);
      await this.get("questionStore.saveQuestion").perform(question);
    }
  }
});
