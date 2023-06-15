import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class CommunicationsIndexRoute extends Route {
  @service ebauModules;

  model() {
    return this.modelFor(
      this.ebauModules.resolveModuleRoute("communications", "communications")
    );
  }
}
