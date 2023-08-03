import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { dropTask } from "ember-concurrency";
import { findRecord } from "ember-data-resources";
import { confirmTask } from "ember-ebau-core/decorators";

export default class CorrectionsController extends Controller {
  @service fetch;
  @service intl;
  @service notification;

  instance = findRecord(this, "instance", () => this.model);

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
      yield this.fetch.fetch(`/api/v1/instances/${this.model}/correction`, {
        method: "POST",
      });

      // sadly we need this to have current data on the whole page
      location.reload();
    } catch (error) {
      this.notification.danger(this.intl.t("corrections.document.error"));
    }
  }
}
