import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class StatisticsAvgCycleTimeRoute extends Route {
  @service can;

  queryParams = { procedure: { refresh: true } };

  redirect() {
    if (this.can.cannot("view statistics", "cycle-time")) {
      this.replaceWith("statistics.index");
    }
  }

  setupController(controller, model) {
    super.setupController(controller, model);

    controller.fetchCycleTimes.perform();
  }

  resetController(controller, isExiting) {
    if (isExiting) {
      controller.procedure = "";
    }
  }
}
