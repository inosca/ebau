import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import {
  dropTask,
  restartableTask,
  lastValue,
  timeout,
  waitForProperty,
} from "ember-concurrency";
import { saveAs } from "file-saver";

import isProd from "camac-ng/utils/is-prod";

export default class DossierImportDetailController extends Controller {
  @service intl;
  @service notification;
  @service store;
  @service router;
  @service fetch;

  @tracked user;

  @lastValue("fetchImport") import;
  @dropTask
  *fetchImport() {
    try {
      this.notification.clear();

      return yield this.store.findRecord("dossier-import", this.model, {
        include: "user",
        reload: true,
      });
    } catch (e) {
      console.error(e);
      this.notification.danger(
        this.intl.t("dossierImport.detail.fetchImportError")
      );
      this.router.transitionTo("index");
    }
  }

  @dropTask
  *deleteImport() {
    try {
      this.notification.clear();

      yield this.import.destroyRecord();

      this.notification.success(
        this.intl.t("dossierImport.detail.actions.deleteImport.success")
      );
      this.router.transitionTo("dossier-import.index");
    } catch (e) {
      console.error(e);
      this.notification.danger(
        this.intl.t("dossierImport.detail.actions.deleteImport.error")
      );
    }
  }

  @dropTask
  *startImport() {
    try {
      this.notification.clear();

      yield this.import.start();

      yield this.fetchImport.perform();

      // success notification only shown until next refresh
      this.notification.success(
        this.intl.t("dossierImport.detail.actions.startImport.success")
      );

      this.refresh.perform();
    } catch (e) {
      console.error(e);
      this.notification.danger(
        this.intl.t("dossierImport.detail.actions.startImport.error")
      );
    }
  }

  @dropTask
  *confirmImport() {
    try {
      this.notification.clear();

      yield this.import.confirm();

      yield this.fetchImport.perform();

      this.notification.success(
        this.intl.t("dossierImport.detail.actions.confirmImport.success")
      );
    } catch (e) {
      console.error(e);
      this.notification.danger(
        this.intl.t("dossierImport.detail.actions.confirmImport.error")
      );
    }
  }

  @dropTask
  *undoImport() {
    try {
      this.notification.clear();

      yield this.import.undo();

      this.notification.success(
        this.intl.t("dossierImport.detail.actions.undoImport.success")
      );
      this.router.transitionTo("dossier-import.index");
    } catch (e) {
      console.error(e);
      this.notification.danger(
        this.intl.t("dossierImport.detail.actions.undoImport.error")
      );
    }
  }

  @dropTask
  *cleanImport() {
    try {
      this.notification.clear();

      yield this.import.clean();
      yield this.fetchImport.perform();

      this.notification.success(
        this.intl.t("dossierImport.detail.actions.cleanImport.success")
      );
    } catch (e) {
      console.error(e);
      this.notification.danger(
        this.intl.t("dossierImport.detail.actions.cleanImport.error")
      );
    }
  }

  @dropTask
  *transmitImport() {
    try {
      this.notification.clear();

      yield this.import.transmit();

      yield this.fetchImport.perform();

      this.notification.success(
        this.intl.t("dossierImport.detail.actions.transmitImport.success")
      );

      this.refresh.perform();
    } catch (e) {
      console.error(e);
      this.notification.danger(
        this.intl.t("dossierImport.detail.actions.transmitImport.error")
      );
    }
  }

  @dropTask
  *downloadImport() {
    try {
      const response = yield this.fetch.fetch(
        `/api/v1/dossier-imports/${this.model}/download`
      );
      saveAs(yield response.blob(), this.import.filename);
    } catch (e) {
      console.error(e);
      this.notification.danger(
        this.intl.t("dossierImport.detail.actions.downloadImport.error")
      );
    }
  }

  @restartableTask
  *refresh() {
    // needed after page reloads because import fetching
    // isn't awaited in setupController
    yield waitForProperty(this.fetchImport, "isRunning", false);

    while (["in-progress", "transmitting"].includes(this.import?.status)) {
      yield timeout(5000);
      yield this.fetchImport.perform();
    }
  }

  get summary() {
    const messages = this.import?.messages;
    return this.isValidated
      ? messages?.validation.summary
      : this.isImported
      ? messages?.import.summary
      : null;
  }

  get progress() {
    return this.import?.messages?.import?.details.length;
  }

  get total() {
    return this.import?.messages?.validation?.summary?.stats?.dossiers;
  }

  get isValidated() {
    return (
      this.import?.status === "verified" || this.import?.status === "failed"
    );
  }

  get isImported() {
    return this.import?.status === "imported";
  }

  get isProd() {
    return isProd();
  }
}
