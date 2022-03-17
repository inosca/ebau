import Route from "@ember/routing/route";
import { macroCondition, getOwnConfig } from "@embroider/macros";

export default class PublicInstancesDetailIndexRoute extends Route {
  redirect() {
    const redirectTo = macroCondition(getOwnConfig().features.publication.form)
      ? "public-instances.detail.form"
      : "public-instances.detail.documents";

    this.replaceWith(redirectTo);
  }
}
