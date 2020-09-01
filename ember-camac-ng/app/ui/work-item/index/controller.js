import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency-decorators";

import createWorkItem from "../../../gql/mutations/create-work-item";

export default class WorkItemIndexController extends Controller {
  queryParams = ["case"];

  @service store;
  @service apollo;
  @service notifications;
  @service intl;
  @service shoebox;

  @tracked services = [];
  @tracked users = [];

  @tracked case;
  @tracked responsibleService = "";
  @tracked responsibleUser = "";
  @tracked title = "";
  @tracked description = "";
  @tracked deadline = new Date();
  @tracked notificationCompleted = true;
  @tracked notificationDeadline = true;

  @dropTask
  *getData() {
    const instance = yield this.store.findRecord(
      "instance",
      this.shoebox.content.entrypoint.models[0].id,
      { include: "involved_services" }
    );
    const users = yield this.store.query("user", {
      service: instance.involvedServices.map(service => service.id).join(",")
    });

    this.services = instance.involvedServices;
    this.users = users;
  }

  @dropTask
  *createWorkItem() {
    try {
      yield this.apollo.mutate({
        mutation: createWorkItem,
        variables: {
          input: {
            case: this.case,
            multipleInstanceTask: "create-manual-workitems",
            name: this.title,
            description: this.description,
            addressedGroups: [this.responsibleService.id],
            assignedUsers: [this.responsibleUser.username],
            deadline: this.deadline,
            meta: JSON.stringify({
              "notify-complete": this.notificationCompleted,
              "notify-deadline": this.notificationDeadline
            })
          }
        }
      });
    } catch (error) {
      this.notifications.error(this.intl.t("workItemList.all.saveError"));
    }
  }

  get selectedOwnService() {
    return (
      this.responsibleService.id === this.shoebox.content.serviceId.toString()
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
}
