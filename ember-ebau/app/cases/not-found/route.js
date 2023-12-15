import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class CasesNotFoundRoute extends Route {
  @service store;

  async model() {
    // has to fetch the resources because it gets loaded before the navigation
    return (await this.store.findAll("resource")).find((resource) =>
      resource.link.includes("case"),
    );
  }
}
