import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class LinkedInstancesRoute extends Route {
  @service ebauModules;
  @service store;

  async model() {
    /* ember-ebau already prefetches the record, so we can simply peek it.
     * ember-camac-ng does not, so we need to fetch it here.
     */
    return this.ebauModules.isLegacyApp
      ? await this.store.findRecord("instance", this.ebauModules.instanceId, {
          include: "linkedInstances",
        })
      : this.store.peekRecord("instance", this.ebauModules.instanceId);
  }
}
