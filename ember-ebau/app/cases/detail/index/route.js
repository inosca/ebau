import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class CasesDetailIndexRoute extends Route {
  @service router;
  @service store;

  async redirect() {
    const instanceId = this.modelFor("cases.detail").id;
    const first = (
      await this.store.query("instance-resource", {
        instance: this.modelFor("cases.detail").id,
        "page[size]": 1,
        "page[number]": 1,
      })
    )[0];

    if (first) {
      this.router.replaceWith(`/cases/${instanceId}/${first.link}`);
    }
  }
}
