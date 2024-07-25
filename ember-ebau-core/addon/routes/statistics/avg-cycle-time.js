import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class StatisticsAvgCycleTimeRoute extends Route {
  @service abilities;
  @service router;

  queryParams = { procedure: { refresh: true } };

  redirect() {
    if (this.abilities.cannot("view statistics", "cycle-time")) {
      this.router.replaceWith("statistics.index");
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
