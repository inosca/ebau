import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class CasesDetailRoute extends Route {
  @service alexandriaConfig;
  @service ebauModules;
  @service store;
  @service router;
  @service permissions;

  async model({ instance_id }) {
    this.alexandriaConfig.instanceId = parseInt(instance_id);
    this.ebauModules.instanceId = parseInt(instance_id);

    try {
      // fetch instance to allow reloading after state changes
      // from ebau-modules.js (redirectToWorkItems)
      return await this.store.findRecord("instance", instance_id, {
        include: "instance_state,responsible_service_users,linked_instances",
      });
    } catch (error) {
      console.error(error);
      this.router.transitionTo("cases.not-found");
    }
  }

  async afterModel() {
    if (this.permissions.fullyEnabled) {
      await this.permissions.populateCacheFor(this.ebauModules.instanceId);
    }
  }
}
