import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";
import { trackedTask } from "reactiveweb/ember-concurrency";

export default class PublicInstancesDetailController extends Controller {
  @service store;
  @service notification;
  @service intl;

  queryParams = ["key"];

  @tracked key = null;

  publicInstance = trackedTask(this, this.fetchPublicInstance, () => [
    this.model,
    this.key,
  ]);

  @dropTask
  *fetchPublicInstance() {
    yield Promise.resolve();

    try {
      const instances = yield this.store.query("public-caluma-instance", {
        instance: this.model,
      });

      return instances[0];
    } catch (e) {
      this.notification.danger(this.intl.t("publicInstancesDetail.loadError"));
    }
  }
}
