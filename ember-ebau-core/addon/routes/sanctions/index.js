import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class SanctionsIndexRoute extends Route {
  @service ebauModules;
  @service store;

  async model() {
    return await this.store.findRecord("instance", this.ebauModules.instanceId);
  }
}
