import Route from "@ember/routing/route";
import { service } from "@ember/service";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";

export default class NewCaseRoute extends Route {
  @service router;

  async beforeModel() {
    if (!hasFeature("internalCaseCreation")) {
      this.router.transitionTo("cases.not-found");
    }
  }
}
