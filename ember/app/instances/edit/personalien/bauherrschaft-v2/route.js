import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class InstancesEditPersonalienBauherrschaftController extends Route {
  @service("question-store") questionStore;

  setupController(controller, model) {
    super.setupController(controller, model);
    const question = this.questionStore.peek(
      "grundeigentumerschaft",
      model.instance.get("id")
    );
    controller.set(
      "grundeigentumerschaftValue",
      question ? question.get("value") : []
    );
  }
}
