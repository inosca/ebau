import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";

export default class PublicInstancesDetailFormRoute extends Route {
  @service router;

  redirectTo() {
    if (!hasFeature("publication.form")) {
      return this.router.replaceWith("public-instances.detail.index");
    }
  }
}
