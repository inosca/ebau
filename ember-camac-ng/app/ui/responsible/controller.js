import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";

export default class ResponsibleController extends Controller {
  @service store;
  @service shoebox;
  @service notifications;
  @service intl;

  @tracked _selectedUser;
  @tracked responsibilities = [];
  @tracked users = [];

  get current() {
    return this.responsibilities.find(
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
    this.responsibilities = yield this.store.query("responsible-service", {
      instance: this.model.id,
      include: "responsible_user,service",
    });

    this.users = yield this.store.query("user", {
      service: this.shoebox.content.serviceId,
    });
  }

  @dropTask
  *saveResponsibility(event) {
    event.preventDefault();

    try {
      const responsibility =
        this.current ||
        this.store.createRecord("responsible-service", {
          instance: this.model,
        });

      responsibility.responsibleUser = this.selectedUser;

      yield responsibility.save();
      yield this.fetchData.perform();

      this.notifications.success(this.intl.t("responsible.saveSuccess"));
    } catch (error) {
      this.notifications.error(this.intl.t("responsible.saveError"));
    }
  }
}
