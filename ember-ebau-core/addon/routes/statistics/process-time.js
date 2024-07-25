import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class StatisticsProcessTimeRoute extends Route {
  @service abilities;
  @service router;

  redirect() {
    if (this.abilities.cannot("view statistics", "process-time")) {
      this.router.replaceWith("statistics.index");
    }
  }
}
