import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class RulesetsDistributionDeadlineNewRoute extends Route {
  @service store;

  model() {
    return this.store.createRecord("distribution-deadline-rule");
  }

  resetController(controller, isExiting) {
    if (isExiting) {
      // Make sure that canceling the creation removes the new record
      controller.model.rollbackAttributes();
    }
  }
}
