import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { dropTask, lastValue } from "ember-concurrency-decorators";

export default class PublicInstancesDetailController extends Controller {
  @service store;
  @service notification;
  @service intl;

  @lastValue("getPublicAttachments") attachments;
  @dropTask
  *getPublicAttachments() {
    try {
      return yield this.store.query("attachment", {
        instance: this.model,
        context: JSON.stringify({
          key: "isPublished",
          value: true,
        }),
      });
    } catch (e) {
      this.notification.danger(this.intl.t("publicInstancesDetail.loadError"));
    }
  }
}
