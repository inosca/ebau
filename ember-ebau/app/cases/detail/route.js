import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class CasesDetailRoute extends Route {
  @service alexandriaConfig;
  @service ebauModules;
  @service store;

  model({ instance_id }) {
    // fetch instance to allow reloading after state changes
    // from ebau-modules.js (redirectToWorkItems)
    return this.store.findRecord("instance", instance_id);
  }

  afterModel(model) {
    if (typeof model === "object") {
      model = parseInt(model.id);
    }
    this.alexandriaConfig.instanceId = model;
    this.ebauModules.instanceId = model;
  }
}
