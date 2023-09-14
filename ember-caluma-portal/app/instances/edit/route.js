import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class InstancesEditRoute extends Route {
  @service config;
  @service ebauModules;

  model({ instance }) {
    return parseInt(instance);
  }

  afterModel(instanceId) {
    this.config.instanceId = instanceId;
    this.ebauModules.instanceId = instanceId;
  }

  setupController(controller, ...args) {
    super.setupController(controller, ...args);

    this.ebauModules.onAdditionalDemandComplete =
      controller.additionalDemandsCount.reload;
  }
}
