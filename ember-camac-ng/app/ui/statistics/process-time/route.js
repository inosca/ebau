import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class StatisticsProcessTimeRoute extends Route {
  @service can;

  redirect() {
    if (this.can.cannot("view statistics", "process-time")) {
      this.replaceWith("statistics.index");
    }
  }

  setupController(controller, model) {
    super.setupController(controller, model);

    controller.fetchActivationsSummary.perform();
  }
}
