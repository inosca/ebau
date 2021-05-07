import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency-decorators";

export default class ResponsibleController extends Controller {
  @service store;
  @service shoebox;
  @service notifications;
  @service intl;
  @service can;

  @tracked _selectedUser;

  get responsibilites() {
    return this.store
      .peekAll("responsible-service")
      .filter(
        (responsibleService) =>
          parseInt(responsibleService.belongsTo("instance").id()) ===
          parseInt(this.model.id)
      );
  }

  get users() {
    return this.store
      .peekAll("user")
      .filter(
        (user) =>
          parseInt(user.belongsTo("service").id()) ===
          this.shoebox.content.serviceId
      );
  }

  get current() {
    return this.responsibilites.find(
      (responsibleService) =>
        parseInt(responsibleService.belongsTo("service").id()) ===
        this.shoebox.content.serviceId
    );
  }

  get selectedUser() {
    return this._selectedUser || this.current?.responsibleUser;
  }

  set selectedUser(user) {
    this._selectedUser = user;
  }

  @dropTask
  *fetchData() {
    yield this.store.query("responsible-service", {
      instance: this.model.id,
      include: "responsible_user,service",
    });

    yield this.store.query("user", {
      service: this.shoebox.content.serviceId,
    });
  }

  @dropTask
  *saveResponsibility(event) {
    event.preventDefault();

    if (this.can.cannot("edit responsible-service")) {
      return;
    }

    try {
      const responsibility =
        this.current ||
        this.store.createRecord("responsible-service", {
          instance: this.model,
        });

      responsibility.responsibleUser = this.selectedUser;

      yield responsibility.save();

      this.notifications.success(this.intl.t("responsible.saveSuccess"));
    } catch (error) {
      this.notifications.error(this.intl.t("responsible.saveError"));
    }
  }
}
