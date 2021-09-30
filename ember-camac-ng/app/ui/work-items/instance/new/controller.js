import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency-decorators";
import moment from "moment";

import ENV from "camac-ng/config/environment";
import createWorkItem from "camac-ng/gql/mutations/create-work-item.graphql";
import allCases from "camac-ng/gql/queries/all-cases.graphql";

class NewWorkItem {
  @tracked case;
  @tracked addressedGroups = [];
  @tracked assignedUsers = [];
  @tracked title = "";
  @tracked description = "";
  @tracked deadline = moment().add(10, "days");
  @tracked notificationCompleted = true;
  @tracked notificationDeadline = true;
}

export default class WorkItemNewController extends Controller {
  @queryManager apollo;

  @service store;
  @service notifications;
  @service intl;
  @service shoebox;

  @tracked instance = null;
  @tracked case = null;
  @tracked users = [];

  @tracked workItem = new NewWorkItem();

  get responsibleService() {
    return this.services.find((service) =>
      this.workItem.addressedGroups.includes(service.id)
    );
  }

  set responsibleService(service) {
    this.workItem.addressedGroups = [String(service.id)];

    if (parseInt(service.id) !== this.shoebox.content.serviceId) {
      this.workItem.assignedUsers = [];
    }
  }

  get responsibleUser() {
    return this.users.find((user) =>
      this.workItem.assignedUsers.includes(user.username)
    );
  }

  set responsibleUser(user) {
    this.workItem.assignedUsers = [user.username];
  }

  get selectedOwnService() {
    return (
      parseInt(this.responsibleService?.id) === this.shoebox.content.serviceId
    );
  }

  get services() {
    const services = this.instance?.involvedServices.toArray() || [];

    if (ENV.APPLICATION.allowApplicantManualWorkItem) {
      services.unshift({
        id: "applicant",
        name: this.intl.t("global.applicant"),
      });
    }

    return services;
  }

  @dropTask
  *getData() {
    this.instance = yield this.store.findRecord("instance", this.model.id, {
      include: "involved_services",
      reload: true,
    });

    this.users = yield this.store.query("user", {
      service: this.shoebox.content.serviceId,
    });

    this.case = yield this.apollo.query(
      {
        query: allCases,
        variables: {
          metaValueFilter: [{ key: "camac-instance-id", value: this.model.id }],
        },
      },
      "allCases.edges.firstObject.node.id"
    );
  }

  @dropTask
  *createWorkItem(event) {
    event.preventDefault();

    const extra = {
      ...(this.workItem.assignedUsers.length
        ? { assignedUsers: this.workItem.assignedUsers }
        : {}),
      ...(!this.selectedOwnService
        ? { controllingGroups: [String(this.shoebox.content.serviceId)] }
        : {}),
    };

    try {
      yield this.apollo.mutate({
        mutation: createWorkItem,
        variables: {
          input: {
            case: this.case,
            multipleInstanceTask: "create-manual-workitems",
            name: this.workItem.title,
            description: this.workItem.description,
            addressedGroups: this.workItem.addressedGroups,
            deadline: this.workItem.deadline,
            meta: JSON.stringify({
              "notify-completed": this.workItem.notificationCompleted,
              "notify-deadline": this.workItem.notificationDeadline,
              "is-manually-completable": true,
            }),
            ...extra,
          },
        },
      });

      this.workItem = new NewWorkItem();

      this.notifications.success(this.intl.t("workItems.saveSuccess"));

      this.transitionToRoute("work-items.instance.index");
    } catch (error) {
      this.notifications.error(this.intl.t("workItems.saveError"));
    }
  }

  @action
  setDeadline(value) {
    this.workItem.deadline = value;
  }
}
