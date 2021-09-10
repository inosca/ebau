import Controller, { inject as controller } from "@ember/controller";
import { inject as service } from "@ember/service";
import { dropTask, lastValue } from "ember-concurrency-decorators";

export default class PublicInstancesDetailDocumentsController extends Controller {
  @service store;
  @service notification;
  @service intl;

  @controller("public-instances.detail") detailController;

  get dossierNr() {
    return this.detailController.publicInstance?.dossierNr;
  }

  @lastValue("fetchPublicAttachments") attachments;
  @dropTask
  *fetchPublicAttachments() {
    try {
      return yield this.store.query("attachment", {
        instance: this.model,
      });
    } catch (e) {
      this.notification.danger(this.intl.t("publicInstancesDetail.loadError"));
    }
  }
}
