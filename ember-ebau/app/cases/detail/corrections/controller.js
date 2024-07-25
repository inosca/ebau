import Controller from "@ember/controller";
import { action } from "@ember/object";
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

  @action
  toggleModal() {
    this.showModal = !this.showModal;
  }

  @dropTask
  @confirmTask("corrections.document.confirm")
  *startCorrection() {
    yield this.documentCorrection.perform();
  }

  @dropTask
  *documentCorrection() {
    try {
      yield this.fetch.fetch(`/api/v1/instances/${this.model.id}/correction`, {
        method: "POST",
      });

      // sadly we need this to have current data on the whole page
      location.reload();
    } catch (error) {
      if (error.cause) {
        this.notification.danger(error.cause.map((e) => e.detail).join("<br>"));
      } else {
        this.notification.danger(this.intl.t("corrections.document.error"));
      }
    }
  }

  @dropTask
  @confirmTask("corrections.withdraw.confirm")
  *withdrawInstance() {
    try {
      yield this.fetch.fetch(`/api/v1/instances/${this.model.id}/withdraw`, {
        method: "POST",
      });

      this.notification.success(this.intl.t("corrections.withdraw.success"));

      yield this.ebauModules.redirectToWorkItems();
    } catch (error) {
      this.notification.danger(this.intl.t("corrections.withdraw.error"));
    }
  }
}
