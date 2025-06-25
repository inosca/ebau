import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { findRecord, query, findAll } from "ember-data-resources";
import { DateTime } from "luxon";

import mainConfig from "ember-ebau-core/config/main";
import createWorkItem from "ember-ebau-core/gql/mutations/create-work-item.graphql";
import allCases from "ember-ebau-core/gql/queries/all-cases.graphql";

class NewWorkItem {
  @tracked case;
  @tracked addressedGroups = [];
  @tracked assignedUsers = [];
  @tracked title = "";
  @tracked description = "";
  @tracked deadline = DateTime.now().plus({ days: 10 }).toJSDate();
  @tracked notificationCompleted = true;
  @tracked notificationDeadline = true;
  @tracked meta = {};
}

export default class WorkItemDetailNewComponent extends Component {
  @queryManager apollo;

  @service store;
  @service intl;
  @service router;
  @service ebauModules;
  @service notification;

  @tracked workItem = new NewWorkItem();
  @tracked selectedTemplate = null;

  workItemTemplates = findAll(this, "work-item-template", () => ({
    include: "assigned_user",
  }));

  get responsibleService() {
    return this.services.find((service) =>
      this.workItem.addressedGroups.includes(service.id),
    );
  }

  set responsibleService(service) {
    this.workItem.addressedGroups = [service.id.toString()];

    if (parseInt(service.id) !== this.args.serviceId) {
      this.workItem.assignedUsers = [];
    }
  }

  get responsibleUser() {
    return this.users.records?.find((user) =>
      this.workItem.assignedUsers.includes(user.username),
    );
  }

  set responsibleUser(user) {
    this.workItem.assignedUsers = [user.username];
  }

  get selectedOwnService() {
    return (
      parseInt(this.responsibleService?.id) === parseInt(this.args.serviceId)
    );
  }

  get services() {
    const services = [...(this.instance.record?.involvedServices ?? [])];

    if (mainConfig.allowApplicantManualWorkItem) {
      services.unshift({
        id: "applicant",
        name: this.intl.t("global.applicant"),
      });
    }

    return services;
  }

  instance = findRecord(this, "instance", () => [
    this.args.instanceId,
    { include: "involved_services", reload: true },
  ]);

  users = query(this, "public-user", () => ({
    service: this.args.serviceId,
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
        ? { controllingGroups: [this.args.serviceId.toString()] }
        : {}),
    };

    try {
      const caseId = (yield this.apollo.query(
        {
          query: allCases,
          variables: {
            metaValueFilter: [
              { key: "camac-instance-id", value: this.args.instanceId },
            ],
          },
        },
        "allCases.edges",
      ))[0].node.id;

      // Fix until caluma backend runs on python >3.10
      const deadline = this.workItem.deadline
        .toISOString()
        .replace("Z", "+00:00");
      yield this.apollo.mutate({
        mutation: createWorkItem,
        variables: {
          input: {
            case: caseId,
            multipleInstanceTask: "create-manual-workitems",
            name: this.workItem.title,
            description: this.workItem.description,
            addressedGroups: this.workItem.addressedGroups,
            deadline,
            meta: JSON.stringify({
              "notify-completed": this.workItem.notificationCompleted,
              "notify-deadline": this.workItem.notificationDeadline,
              "is-manually-completable": true,
              ...this.workItem.meta,
            }),
            ...extra,
          },
        },
      });

      this.workItem = new NewWorkItem();

      this.notification.success(this.intl.t("workItems.saveSuccess"));

      this.router.transitionTo(`${this.args.baseRoute}.index`);
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("workItems.saveError"));
    }
  }

  @action
  applyTemplate() {
    if (!this.selectedTemplate) {
      return;
    }

    const rule = this.selectedTemplate.responsibilityRule;
    const currentService = rule !== "NONE";
    const bypassResponsible = rule === "NO_USER";

    let assignedUsers = [];

    if (rule === "CURRENT_USER") {
      assignedUsers = [this.ebauModules.userName];
    } else if (rule === "SPECIFIC_USER") {
      assignedUsers = [
        this.selectedTemplate.get("assignedUser.username"),
      ].filter(Boolean);
    }

    this.workItem.title = this.selectedTemplate.name;
    this.workItem.description = this.selectedTemplate.description;
    this.workItem.meta = {
      "template-id": this.selectedTemplate.id,
      "bypass-responsible-user": bypassResponsible,
    };
    this.workItem.deadline = DateTime.now()
      .plus({ days: this.selectedTemplate.leadTime ?? 10 })
      .toJSDate();
    this.workItem.addressedGroups = currentService
      ? [this.args.serviceId.toString()]
      : [];
    this.workItem.assignedUsers = assignedUsers;
  }
}
