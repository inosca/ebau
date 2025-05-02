import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class RulesetsDistributionDeadlineEditRoute extends Route {
  @service store;

  model({ id }) {
    return this.store.findRecord("distribution-deadline-rule", id, {
      include: "target_service",
    });
  }
}
