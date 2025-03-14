import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class SanctionsNewRoute extends Route {
  @service store;
  @service ebauModules;

  async model() {
    const instance = await this.store.findRecord(
      "instance",
      this.ebauModules.instanceId,
    );
    return this.store.createRecord("sanction", {
      instance,
    });
  }
}
