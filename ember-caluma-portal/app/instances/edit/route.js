import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class InstancesEditRoute extends Route {
  @service alexandriaConfig;
  @service ebauModules;

  model({ instance }) {
    return parseInt(instance);
  }

  afterModel(instanceId) {
    this.alexandriaConfig.instanceId = instanceId;
    this.ebauModules.instanceId = instanceId;
  }

  setupController(controller, ...args) {
    super.setupController(controller, ...args);

    this.ebauModules.onAdditionalDemandComplete =
      controller.additionalDemandsCount.reload;

    controller.reload();
  }
}
