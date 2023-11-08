import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class ResponsibleRoute extends Route {
  @service ebauModules;

  model() {
    return this.ebauModules.instanceId;
  }

  resetController(controller, isExiting) {
    if (isExiting) {
      controller._selectedUser = null;
      controller.responsibilities = [];
      controller.users = [];
    }
  }
}
