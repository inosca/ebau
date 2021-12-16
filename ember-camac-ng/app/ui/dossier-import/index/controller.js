import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { dropTask, lastValue } from "ember-concurrency-decorators";

export default class DossierImportIndexController extends Controller {
  @service intl;
  @service notifications;
  @service store;
  @service shoebox;
  @service session;
  @service fetch;

  @lastValue("fetchImports") imports;
  @dropTask
  *fetchImports() {
    try {
      return yield this.store.query("dossier-import", {
        include: "user",
        page: {
          size: 10,
        },
      });
    } catch (e) {
      this.notifications.error(
        this.intl.t("dossierImport.imports.fetchImportsError")
      );
    }
  }

  @action
  clearNotifications() {
    this.notifications.clear();
  }
}
