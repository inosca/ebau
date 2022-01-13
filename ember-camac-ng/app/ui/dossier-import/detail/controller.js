import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { timeout, waitForProperty } from "ember-concurrency";
import {
  dropTask,
  restartableTask,
  lastValue,
} from "ember-concurrency-decorators";

export default class DossierImportDetailController extends Controller {
  @service intl;
  @service notifications;
  @service store;
  @service router;

  @tracked user;

  @lastValue("fetchImport") import;
  @dropTask
  *fetchImport() {
    try {
      this.notifications.clear();

      return yield this.store.findRecord("dossier-import", this.model, {
        include: "user",
        reload: true,
      });
    } catch (e) {
      this.notifications.error(
        this.intl.t("dossierImport.detail.fetchImportError")
      );
      this.router.transitionTo("index");
    }
  }

  @dropTask
  *deleteImport() {
    try {
      this.notifications.clear();

      yield this.import.destroyRecord();

      this.notifications.success(
        this.intl.t("dossierImport.detail.actions.deleteImport.success")
      );
      this.router.transitionTo("dossier-import.index");
    } catch (e) {
      this.notifications.error(
        this.intl.t("dossierImport.detail.actions.deleteImport.error")
      );
    }
  }

  @dropTask
  *startImport() {
    try {
      this.notifications.clear();

      yield this.import.start();

      yield this.fetchImport.perform();

      // success notification only shown until next refresh
      this.notifications.success(
        this.intl.t("dossierImport.detail.actions.startImport.success")
      );

      this.refresh.perform();
    } catch (e) {
      this.notifications.error(
        this.intl.t("dossierImport.detail.actions.startImport.error")
      );
    }
  }

  @restartableTask
  *refresh() {
    // needed after page reloads because import fetching
    // isn't awaited in setupController
    yield waitForProperty(this.fetchImport, "isRunning", false);

    while (this.import?.status === "in-progress") {
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

  get isValidated() {
    return (
      this.import?.status === "verified" || this.import?.status === "failed"
    );
  }

  get isImported() {
    return this.import?.status === "done";
  }
}
