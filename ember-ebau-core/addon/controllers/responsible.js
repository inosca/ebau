import Controller from "@ember/controller";
import { service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { task } from "ember-concurrency";
import { query } from "ember-data-resources";

export default class ResponsibleController extends Controller {
  @service store;
  @service ebauModules;
  @service notification;
  @service intl;

  @tracked _selectedUser;

  users = query(this, "user", () => ({
    service: this.ebauModules.serviceId,
    sort: "name,surname",
  }));

  responsibilities = query(this, "responsible-service", () => ({
    instance: this.model,
    include: "responsible_user,service",
  }));

  get current() {
    return this.responsibilities.records?.find(
      (responsibleService) =>
        parseInt(responsibleService.belongsTo("service").id()) ===
        this.ebauModules.serviceId,
    );
  }

  get selectedUser() {
    return this._selectedUser || this.current?.responsibleUser;
  }

  set selectedUser(user) {
    this._selectedUser = user;
  }

  saveResponsibility = task({ drop: true }, async (event) => {
    event.preventDefault();

    try {
      const responsibility =
        this.current ??
        this.store.createRecord("responsible-service", {
          instance: await this.store.findRecord("instance", this.model),
        });

      responsibility.responsibleUser = this.selectedUser;

      await responsibility.save();
      await this.responsibilities.retry();
      await this.store.findRecord("instance", this.model);

      this.notification.success(this.intl.t("responsible.saveSuccess"));
    } catch {
      this.notification.danger(this.intl.t("responsible.saveError"));
    }
  });
}
