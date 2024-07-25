import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class StaticContentRoute extends Route {
  @service ebauModules;

  model({ type }) {
    return { instanceId: this.ebauModules.instanceId, type };
  }
}
