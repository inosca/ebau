import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class StatisticsProcessTimeRoute extends Route {
  @service can;
  @service router;

  redirect() {
    if (this.can.cannot("view statistics", "process-time")) {
      this.router.replaceWith("statistics.index");
    }
  }
}
