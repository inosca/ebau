import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency-decorators";

export default class ResponsibleController extends Controller {
  @service store;
  @service shoebox;
  @service notifications;
  @service intl;

  @tracked selectedUser;
  @tracked fetchedUsers = [];
  @tracked responsibilites = [];

  @dropTask
  *getData() {
    this.responsibilites = yield this.store.query("responsible-service", {
      instance: this.model.id,
      include: "responsible_user,service",
    });

    this.fetchedUsers = yield this.store.query("user", {
      service: this.shoebox.content.serviceId,
    });

    this.selectedUser = yield this.responsibilites.find(
      (res) =>
        parseInt(res.get("service.id")) === this.shoebox.content.serviceId
    )?.responsibleUser;
  }

  @dropTask
  *saveResponsibility(event) {
    event.preventDefault();

    try {
      let responsibility = this.responsibilites.find(
        (res) =>
          parseInt(res.get("service.id")) === this.shoebox.content.serviceId
      );

      if (!responsibility) {
        responsibility = this.store.createRecord("responsible-service", {
          instance: this.model,
          service_id: this.shoebox.content.serviceId,
        });
      }

      responsibility.responsibleUser = this.selectedUser;
      yield responsibility.save();

      this.responsibilites.update();
      this.selectedUser = {};

      this.notifications.success(this.intl.t("responsible.saveSuccess"));
    } catch (error) {
      this.notifications.error(this.intl.t("responsible.saveError"));
    }
  }
}
