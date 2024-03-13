import Controller, { inject as controller } from "@ember/controller";
import { inject as service } from "@ember/service";
import { dropTask } from "ember-concurrency";
import mainConfig from "ember-ebau-core/config/main";
import { trackedTask } from "reactiveweb/ember-concurrency";

export default class PublicInstancesDetailDocumentsController extends Controller {
  @service store;
  @service notification;
  @service intl;

  @controller("public-instances.detail") detailController;

  get dossierNr() {
    return this.detailController.publicInstance.value?.dossierNr;
  }

  attachments = trackedTask(this, this.fetchAttachments, () => [this.model]);

  @dropTask
  *fetchAttachments() {
    yield Promise.resolve();

    try {
      if (mainConfig.documentBackend === "camac") {
        return yield this.store.query("attachment", {
          instance: this.model,
        });
      }
      return yield this.store.query("document", {
        filter: {
          metainfo: JSON.stringify([
            { key: "camac-instance-id", value: String(this.model) },
          ]),
        },
        sort: "title",
        include: "files,marks",
      });
    } catch (e) {
      this.notification.danger(this.intl.t("publicInstancesDetail.loadError"));
    }
  }
}
