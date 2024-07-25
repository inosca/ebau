import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class CommunicationsIndexRoute extends Route {
  @service ebauModules;

  model() {
    return this.ebauModules.instanceId;
  }
}
