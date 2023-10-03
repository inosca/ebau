import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class IndexRoute extends Route {
  @service router;
  @service store;

  async redirect() {
    const firstResource = (
      await this.store.query("resource", {
        "page[size]": 1,
        "page[number]": 1,
      })
    )[0];

    if (firstResource) {
      return this.router.replaceWith(firstResource.link);
    }
  }
}
