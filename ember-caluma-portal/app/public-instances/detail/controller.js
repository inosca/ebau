import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { dropTask, lastValue } from "ember-concurrency-decorators";

export default class PublicInstancesDetailController extends Controller {
  @service store;
  @service notification;
  @service intl;

  @lastValue("fetchPublicInstance") publicInstance;
  @dropTask
  *fetchPublicInstance() {
    try {
      return (yield this.store.query("public-caluma-instance", {
        instance: this.model,
      }))?.toArray()?.[0];
    } catch (e) {
      this.notification.danger(this.intl.t("publicInstancesDetail.loadError"));
    }
  }
}
