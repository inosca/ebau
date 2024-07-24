import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class CommunicationsNewRoute extends Route {
  @service ebauModules;

  model() {
    return this.ebauModules.instanceId;
  }
}
