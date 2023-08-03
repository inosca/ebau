import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { dropTask } from "ember-concurrency";
import { confirmTask } from "ember-ebau-core/decorators";
import { findRecord } from "ember-data-resources";

export default class CorrectionsController extends Controller {
  @service fetch;
  @service intl;
  @service notification;

  @action
  toggleModal() {
    this.showModal = !this.showModal;
  }

  instance = findRecord(this, "instance", () => this.model);

  @dropTask
  @confirmTask("corrections.document.confirm")
  *documentCorrection() {
    try {
      yield this.fetch.fetch(`/api/v1/instances/${this.model}/correction`, {
        method: "POST",
      });
    } catch (error) {
      this.notification.danger(this.intl.t("corrections.document.error"));
    }
  }
}
