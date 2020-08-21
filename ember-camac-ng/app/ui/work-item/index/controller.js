import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency-decorators";

export default class WorkItemIndexController extends Controller {
  @service store;
  @service apollo;
  @service notifications;
  @service intl;
  @service shoebox;

  @tracked services = [];
  @tracked users = [];

  @tracked responsibleServices = [];
  @tracked responsibleUsers = [];
  @tracked title = "";
  @tracked description = "";
  @tracked deadline = new Date();
  @tracked notificationCompleted = false;
  @tracked notificationDeadline = false;

  @dropTask
  *getData() {
    const instance = yield this.store.findRecord(
      "instance",
      this.shoebox.content.entrypoint.models[0].id,
      { include: "services" }
    );
    const users = yield this.store.query("user", {
      service: instance.services.map(service => service.id).join(",")
    });

    this.services = instance.services;
    this.users = users;
  }

  @dropTask
  *createWorkItem() {
    yield this.apollo.mutate({ mutation: "", variables: { input: {} } });
  }

  get selectedOwnService() {
    return this.responsibleServices?.filterBy(
      "id",
      this.shoebox.content.serviceId.toString()
    );
  }

  get ownServiceUsers() {
    return this.users.filter(
      user =>
        user.service.get("id") === this.shoebox.content.serviceId.toString()
    );
  }

  @action
  setDeadline(value) {
    this.deadline = value;
  }

  @action
  back() {
    history.back();
  }
}
