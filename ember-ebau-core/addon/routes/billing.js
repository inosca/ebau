import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class BillingRoute extends Route {
  @service store;
  @service ebauModules;

  beforeModel() {
    return this.store.findRecord("instance", this.ebauModules.instanceId);
  }
}
