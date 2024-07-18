import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class InstancesEditRoute extends Route {
  @service alexandriaConfig;
  @service ebauModules;
  @service permissions;
  @service store;

  model({ instance }) {
    return parseInt(instance);
  }

  async afterModel(instanceId) {
    this.alexandriaConfig.instanceId = instanceId;
    this.ebauModules.instanceId = instanceId;

    if (this.permissions.fullyEnabled) {
      await this.permissions.populateCacheFor(instanceId);
    }
  }

  setupController(controller, ...args) {
    super.setupController(controller, ...args);

    this.ebauModules.onAdditionalDemandComplete =
      controller.additionalDemandsCount.reload;

    controller.reload();
  }
}
