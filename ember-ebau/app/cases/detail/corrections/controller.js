import Controller from "@ember/controller";
import { service } from "@ember/service";
import { dropTask } from "ember-concurrency";
import { findRecord } from "ember-data-resources";
import { confirmTask } from "ember-ebau-core/decorators";

export default class CorrectionsController extends Controller {
  @service fetch;
  @service intl;
  @service notification;
  @service ebauModules;

  instance = findRecord(this, "instance", () => this.model.id);

  @dropTask
  @confirmTask("corrections.withdraw.confirm")
  *withdrawInstance() {
    try {
      yield this.fetch.fetch(`/api/v1/instances/${this.model.id}/withdraw`, {
        method: "POST",
      });

      this.notification.success(this.intl.t("corrections.withdraw.success"));

      yield this.ebauModules.redirectToWorkItems();
    } catch {
      this.notification.danger(this.intl.t("corrections.withdraw.error"));
    }
  }
}
