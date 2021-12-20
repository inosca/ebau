import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class InstancesEditPersonalienProjektverfasserPlanerController extends Route {
  @service("question-store") questionStore;

  setupController(controller, model) {
    super.setupController(controller, model);
    const question = this.questionStore.peek(
      "bauherrschaft-v2",
      model.instance.get("id")
    );
    controller.set("bauherrschaftValue", question ? question.get("value") : []);
  }
}
