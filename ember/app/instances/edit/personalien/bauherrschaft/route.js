import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default Route.extend({
  questionStore: service("question-store"),

  setupController(controller, model) {
    this._super(...arguments);
    controller.set(
      "value",
      this.questionStore
        .peek("grundeigentumerschaft", model.instance.get("id"))
        .get("value")
    );
  }
});
