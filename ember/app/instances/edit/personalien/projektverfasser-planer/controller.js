import Controller from "@ember/controller";
import { inject as service } from "@ember/service";

export default Controller.extend({
  questionStore: service("question-store"),

  actions: {
    async transfer() {
      let question = await this.questionStore.peek(
        "projektverfasser-planer",
        this.get("model.instance.id")
      );
      question.set("model.value", this.value);
      question.set("value", this.value);
      await this.get("questionStore.saveQuestion").perform(question);
    }
  }
});
