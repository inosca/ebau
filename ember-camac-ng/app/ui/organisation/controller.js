import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { dropTask, lastValue } from "ember-concurrency";

import { loadingTask } from "camac-ng/decorators";

export default class OrganisationController extends Controller {
  @service intl;
  @service notifications;
  @service store;

  @lastValue("fetchService") service;
  @dropTask
  @loadingTask
  *fetchService() {
    return yield this.store.findRecord("service", this.model);
  }

  @dropTask
  @loadingTask
  *save(event) {
    event.preventDefault();

    try {
      this.service.set("description", this.service.name);

      yield this.service.save();

      this.notifications.success(this.intl.t("organisation.saveSuccess"));
    } catch (error) {
      this.notifications.error(this.intl.t("organisation.saveError"));
    }
  }

  @action
  toggleNotifications() {
    this.service.set("notification", this.service.notification);
  }
}
