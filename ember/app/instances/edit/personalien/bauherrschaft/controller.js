import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { computed } from "@ember/object";

export default Controller.extend({
  questionStore: service("question-store"),

  questionActive: computed("model.instance.fields.@each", function() {
    return this.get("model.instance.fields").findBy(
      "name",
      "grundeigentumerschaft"
    );
  }),

  actions: {
    async copyQuestionValue() {
      let question = await this.questionStore.peek(
        "bauherrschaft",
        this.get("model.instance.id")
      );
      question.set(
        "model.value",
        question
          .get("model.value")
          .pushObjects(this.grundeigentumerschaftValue)
          .uniqBy("uuid")
      );
      await this.get("questionStore.saveQuestion").perform(question);
    }
  }
});
