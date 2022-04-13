import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";
import { macroCondition, getOwnConfig } from "@embroider/macros";

export default class PublicInstancesDetailFormRoute extends Route {
  @service router;

  redirectTo() {
    if (macroCondition(getOwnConfig().enablePublicationForm)) {
      // do nothing
    } else {
      return this.router.replaceWith("public-instances.detail.index");
    }
  }
}
