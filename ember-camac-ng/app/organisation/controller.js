import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { dropTask } from "ember-concurrency";
import { findRecord } from "ember-data-resources";

export default class OrganisationController extends Controller {
  @service intl;
  @service notification;
  @service store;
  @service shoebox;

  service = findRecord(this, "service", () => [this.shoebox.content.serviceId]);

  get isMunicipality() {
    return this.shoebox.baseRole === "municipality";
  }

  @dropTask
  *save(event) {
    event.preventDefault();

    try {
      this.service.record.set("description", this.service.record.name);

      yield this.service.record.save();

      this.notification.success(this.intl.t("organisation.saveSuccess"));
    } catch (error) {
      this.notification.danger(this.intl.t("organisation.saveError"));
    }
  }
}
