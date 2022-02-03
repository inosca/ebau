import Controller, { inject as controller } from "@ember/controller";
import { inject as service } from "@ember/service";
import { dropTask } from "ember-concurrency";
import { useTask } from "ember-resources";

export default class PublicInstancesDetailDocumentsController extends Controller {
  @service store;
  @service notification;
  @service intl;

  @controller("public-instances.detail") detailController;

  get dossierNr() {
    return this.detailController.publicInstance.value?.dossierNr;
  }

  attachments = useTask(this, this.fetchAttachments, () => [this.model]);

  @dropTask
  *fetchAttachments() {
    yield Promise.resolve();

    try {
      return yield this.store.query("attachment", {
        instance: this.model,
      });
    } catch (e) {
      this.notification.danger(this.intl.t("publicInstancesDetail.loadError"));
    }
  }
}
