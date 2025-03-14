import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class SanctionsShowRoute extends Route {
  @service store;

  async model({ id }) {
    return await this.store.findRecord("sanction", id, {
      include: "assignedService,controlledByUser",
    });
  }
}
