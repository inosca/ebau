import Controller, { inject as controller } from "@ember/controller";
import { inject as service } from "@ember/service";
import { macroCondition, getOwnConfig } from "@embroider/macros";
import { dropTask } from "ember-concurrency";
import { trackedTask } from "ember-resources/util/ember-concurrency";

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
      if (macroCondition(getOwnConfig().documentBackendCamac)) {
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
