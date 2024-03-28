import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";
import { trackedTask } from "reactiveweb/ember-concurrency";

export default class SupportController extends Controller {
  @tracked municipality = null;

  @service store;
  @service notification;
  @service intl;

  @action
  updateMunicipality(municipality) {
    this.municipality = municipality?.value;
  }

  service = trackedTask(this, this.fetchService, () => [this.municipality]);

  @dropTask
  *fetchService() {
    yield Promise.resolve();

    try {
      return yield this.store.findRecord("public-service", this.municipality);
    } catch (e) {
      console.error(e);
      this.notification.danger(
        this.intl.t("municipality-filter.serviceLoadError"),
      );
    }
  }
}
