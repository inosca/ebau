import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class StatisticsCycleTimeRoute extends Route {
  @service can;

  queryParams = { instance: { refresh: true } };

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
      controller.instance = null;
    }
  }
}
