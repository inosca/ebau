import Route from "@ember/routing/route";
import { macroCondition, getOwnConfig } from "@embroider/macros";

export default class PublicInstancesDetailFormRoute extends Route {
  redirectTo() {
    if (macroCondition(getOwnConfig().features.publication.form)) {
      // do nothing
    } else {
      return this.replaceWith("public-instances.detail.index");
    }
  }
}
