import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";
import { macroCondition, getOwnConfig } from "@embroider/macros";

export default class PublicInstancesDetailIndexRoute extends Route {
  @service router;

  redirect() {
    const redirectTo = macroCondition(getOwnConfig().features.publication.form)
      ? "public-instances.detail.form"
      : "public-instances.detail.documents";

    this.router.replaceWith(redirectTo);
  }
}
