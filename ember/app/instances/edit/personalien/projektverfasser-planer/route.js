import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default Route.extend({
  questionStore: service("question-store"),

  setupController(controller, model) {
    this._super(...arguments);
    let question = this.questionStore.peek(
      "bauherrschaft",
      model.instance.get("id")
    );
    controller.set("bauherrschaftValue", question ? question.get("value") : []);
  }
});
