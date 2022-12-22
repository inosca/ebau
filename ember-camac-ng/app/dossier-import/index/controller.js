import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { dropTask, lastValue } from "ember-concurrency";

import isProd from "camac-ng/utils/is-prod";

export default class DossierImportIndexController extends Controller {
  @service intl;
  @service notification;
  @service store;

  get isProd() {
    return isProd();
  }

  @lastValue("fetchImports") imports;
  @dropTask
  *fetchImports() {
    try {
      return yield this.store.query("dossier-import", {
        include: "user,group",
      });
    } catch (e) {
      this.notification.danger(
        this.intl.t("dossierImport.imports.fetchImportsError")
      );
    }
  }

  @action
  clearNotifications() {
    this.notification.clear();
  }
}
