import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { findRecord, query } from "ember-data-resources";
import { DateTime } from "luxon";

import ENV from "camac-ng/config/environment";
import createWorkItem from "camac-ng/gql/mutations/create-work-item.graphql";
import allCases from "camac-ng/gql/queries/all-cases.graphql";

class NewWorkItem {
  @tracked case;
  @tracked addressedGroups = [];
  @tracked assignedUsers = [];
  @tracked title = "";
  @tracked description = "";
  @tracked deadline = DateTime.now().plus({ days: 10 }).toJSDate();
  @tracked notificationCompleted = true;
  @tracked notificationDeadline = true;
}

export default class WorkItemNewController extends Controller {
  @queryManager apollo;

  @service store;
  @service notifications;
  @service intl;
  @service shoebox;
  @service router;

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
    return this.users.records?.find((user) =>
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
    const services = this.instance.record?.involvedServices.toArray() || [];

    if (ENV.APPLICATION.allowApplicantManualWorkItem) {
      services.unshift({
        id: "applicant",
        name: this.intl.t("global.applicant"),
      });
    }

    return services;
  }

  instance = findRecord(this, "instance", () => [
    this.model.id,
    { include: "involved_services", reload: true },
  ]);

  users = query(this, "public-user", () => ({
    service: this.shoebox.content.serviceId,
    disabled: false,
  }));

  @dropTask
  *createWorkItem(event) {
    event.preventDefault();

    if (!this.workItem.addressedGroups.length) {
      return;
    }

    const extra = {
      ...(this.workItem.assignedUsers.length
        ? { assignedUsers: this.workItem.assignedUsers }
        : {}),
      ...(!this.selectedOwnService
        ? { controllingGroups: [String(this.shoebox.content.serviceId)] }
        : {}),
    };

    try {
      const caseId = (yield this.apollo.query(
        {
          query: allCases,
          variables: {
            metaValueFilter: [
              { key: "camac-instance-id", value: this.model.id },
            ],
          },
        },
        "allCases.edges"
      ))[0].node.id;

      yield this.apollo.mutate({
        mutation: createWorkItem,
        variables: {
          input: {
            case: caseId,
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

      this.router.transitionTo("work-items.instance.index");
    } catch (error) {
      this.notifications.error(this.intl.t("workItems.saveError"));
    }
  }
}
