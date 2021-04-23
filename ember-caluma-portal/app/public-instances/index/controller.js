import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask, lastValue } from "ember-concurrency-decorators";

export default class PublicInstancesIndexController extends Controller {
  @service store;
  @service notification;
  @service intl;

  @tracked page = 1;

  get meta() {
    return this.instances?.meta;
  }

  queryParams = ["page"];

  get pages() {
    return Array.from({ length: this.meta?.pagination.pages }).map(
      (_, i) => i + 1
    );
  }
  @lastValue("getPublicInstances") instances;
  @dropTask
  *getPublicInstances(page) {
    try {
      if (page) {
        this.page = page;
      }
      return yield this.store.query("public-caluma-instance", {
        page: { number: this.page, size: 20 },
      });
    } catch (e) {
      this.notification.danger(this.intl.t("publicInstances.loadError"));
    }
  }
}
