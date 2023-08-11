import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class CasesDetailRoute extends Route {
  @service alexandriaConfig;
  @service ebauModules;

  model({ instance_id }) {
    return parseInt(instance_id);
  }

  afterModel(model) {
    this.alexandriaConfig.instanceId = model;
    this.ebauModules.instanceId = model;
  }
}
