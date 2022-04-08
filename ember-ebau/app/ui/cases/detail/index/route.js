import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class CasesDetailIndexRoute extends Route {
  @service router;

  redirect() {
    this.router.transitionTo("cases.detail.work-items");
  }
}
