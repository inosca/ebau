import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class AdditionalDemandRoute extends Route {
  @service store;
  @service additionalDemand;
  @service ebauModules;

  async model() {
    this.additionalDemand.instanceId = this.ebauModules.instanceId;

    return (
      this.store.peekRecord("instance", this.ebauModules.instanceId) ??
      this.store.findRecord("instance", this.ebauModules.instanceId)
    );
  }
}
