import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class InstancesEditRoute extends Route {
  @service config;

  model({ instance }) {
    return parseInt(instance);
  }

  afterModel(instanceId) {
    this.config.instanceId = instanceId;
  }
}
