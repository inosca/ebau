import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class DeadlinesIndexRoute extends Route {
  @service store;
  @service ebauModules;

  async model() {
    return await this.store.peekRecord("instance", this.ebauModules.instanceId);
  }
}
