import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class PublicationRoute extends Route {
  @service ebauModules;

  model({ type }) {
    return { instanceId: this.ebauModules.instanceId, type };
  }
}
