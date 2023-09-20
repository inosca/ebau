import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class AdditionalDemandIndexRoute extends Route {
  @service additionalDemand;

  model() {
    this.additionalDemand.additionalDemands.value;
  }
}
