import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";
export default class PublicInstancesDetailIndexRoute extends Route {
  @service router;

  redirect() {
    const redirectTo = hasFeature("publication.form")
      ? "public-instances.detail.form"
      : "public-instances.detail.documents";

    this.router.replaceWith(redirectTo);
  }
}
