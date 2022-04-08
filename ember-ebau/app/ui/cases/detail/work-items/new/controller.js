import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { useTask } from "ember-resources";
import { DateTime } from "luxon";

import ENV from "ebau/config/environment";
import createWorkItem from "ebau/gql/mutations/create-work-item.graphql";
import allCases from "ebau/gql/queries/all-cases.graphql";

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

export default class CasesDetailWorkItemsNewController extends Controller {
  @queryManager apollo;

  @service store;
  @service notification;
  @service intl;
  @service session;

  @tracked workItem = new NewWorkItem();

  get responsibleService() {
    return this.services.find((service) =>
      this.workItem.addressedGroups.includes(service.id)
    );
  }

  set responsibleService(service) {
    this.workItem.addressedGroups = [String(service.id)];

    if (parseInt(service.id) !== parseInt(this.session.service.id)) {
      this.workItem.assignedUsers = [];
    }
  }

  get responsibleUser() {
    return this.users.value?.find((user) =>
      this.workItem.assignedUsers.includes(user.username)
    );
  }

  set responsibleUser(user) {
    this.workItem.assignedUsers = [user.username];
  }

  get selectedOwnService() {
    return (
      parseInt(this.responsibleService?.id) ===
      parseInt(this.session.service.id)
    );
  }

  get services() {
    const services = this.instance.value?.involvedServices.toArray() || [];

    if (ENV.APPLICATION.allowApplicantManualWorkItem) {
      services.unshift({
        id: "applicant",
        name: this.intl.t("global.applicant"),
      });
    }

    return services;
  }

  users = useTask(this, this.getUsers, () => [
    this.model,
    this.session.service.id,
  ]);

  instance = useTask(this, this.getInstance, () => [
    this.model,
    this.session.service.id,
  ]);

  @dropTask
  *getUsers() {
    yield Promise.resolve();
    return yield this.store.query("user", {
      service: this.session.service.id,
    });
  }

  @dropTask
  *getInstance() {
    yield Promise.resolve();
    return yield this.store.findRecord("instance", this.model, {
      include: "involved_services",
      reload: true,
    });
  }

  @dropTask
  *getCase() {
    return yield this.apollo.query(
      {
        query: allCases,
        variables: {
          metaValueFilter: [{ key: "camac-instance-id", value: this.model }],
        },
      },
      "allCases.edges.firstObject.node.id"
    );
  }

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
        ? { controllingGroups: [String(this.session.service.id)] }
        : {}),
    };

    const caseId = yield this.getCase.perform();

    try {
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

      this.notification.success(this.intl.t("workItems.saveSuccess"));

      this.transitionToRoute("cases.detail.work-items.index");
    } catch (error) {
      this.notification.danger(this.intl.t("workItems.saveError"));
    }
  }

  @action
  setDeadline(value) {
    this.workItem.deadline = value;
  }
}
