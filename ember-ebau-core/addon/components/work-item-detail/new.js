import { action } from "@ember/object";
import { service } from "@ember/service";
import { macroCondition, getOwnConfig } from "@embroider/macros";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import Changeset from "ember-changeset";
import lookupValidator from "ember-changeset-validations";
import { task } from "ember-concurrency";
import { findRecord, query, findAll } from "ember-data-resources";
import { DateTime } from "luxon";

import mainConfig from "ember-ebau-core/config/main";
import createWorkItem from "ember-ebau-core/gql/mutations/create-work-item.graphql";
import allCases from "ember-ebau-core/gql/queries/all-cases.graphql";
import WorkItemFormValidations from "ember-ebau-core/validations/work-item-form";

export default class WorkItemDetailNewComponent extends Component {
  @queryManager apollo;

  @service store;
  @service intl;
  @service router;
  @service ebauModules;
  @service notification;

  @tracked selectedTemplate = null;

  constructor(...args) {
    super(...args);

    this.model = new Changeset(
      {
        addressedService: null,
        assignedUser: null,
        title: "",
        description: "",
        deadline: DateTime.now().plus({ days: 10 }).toJSDate(),
        notifications: [],
        meta: {},
      },
      lookupValidator(WorkItemFormValidations),
      WorkItemFormValidations,
    );
  }

  getValidationClass = (fi) =>
    fi.isValid ? "uk-form-success" : fi.isInvalid ? "uk-form-danger" : "";

  workItemTemplates = findAll(this, "work-item-template", () => ({
    include: "assigned_user",
  }));

  instance = findRecord(this, "instance", () => [
    this.args.instanceId,
    { include: "involved_services", reload: true },
  ]);

  users = query(this, "public-user", () => ({
    service: this.args.serviceId,
    disabled: false,
  }));

  @action
  updateDescription(fi, event) {
    fi.update(event.target.value);
  }

  get showSnippets() {
    return !this.ebauModules.isApplicant;
  }

  get selectedOwnService() {
    return (
      parseInt(this.model.addressedService?.id) ===
      parseInt(this.args.serviceId)
    );
  }

  get notificationOptions() {
    return [
      {
        key: "completed",
        label: this.intl.t("workItems.notifyCompleted"),
      },
      {
        key: "deadline",
        label: this.intl.t("workItems.notifyDeadline"),
      },
    ];
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

  createWorkItem = task({ drop: true }, async (model) => {
    if (!model.isValid) {
      return;
    }

    const extra = {
      ...(model.assignedUser
        ? { assignedUsers: [model.assignedUser.username] }
        : {}),
      ...(!this.selectedOwnService
        ? { controllingGroups: [this.args.serviceId.toString()] }
        : {}),
    };

    // In Uri we always set a controlling group because otherwise no
    // notifications are sent for manual work-items.
    if (macroCondition(getOwnConfig().application === "ur")) {
      extra.controllingGroups = [this.args.serviceId.toString()];
    }

    try {
      const caseId = await this.apollo.query(
        {
          query: allCases,
          variables: {
            metaValueFilter: [
              { key: "camac-instance-id", value: this.args.instanceId },
            ],
          },
        },
        "allCases.edges.0.node.id",
      );

      await this.apollo.mutate({
        mutation: createWorkItem,
        variables: {
          input: {
            case: caseId,
            multipleInstanceTask: "create-manual-workitems",
            name: model.title,
            description: model.description,
            addressedGroups: [model.addressedService.id],
            deadline: model.deadline,
            meta: JSON.stringify({
              "notify-completed": model.notifications.includes("completed"),
              "notify-deadline": model.notifications.includes("deadline"),
              "is-manually-completable": true,
              ...model.meta,
            }),
            ...extra,
          },
        },
      });

      this.notification.success(this.intl.t("workItems.saveSuccess"));

      this.router.transitionTo(`${this.args.baseRoute}.index`);
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("workItems.saveError"));
    }
  });

  @action
  applyTemplate() {
    if (!this.selectedTemplate) {
      return;
    }

    const rule = this.selectedTemplate.responsibilityRule;
    const currentService = rule !== "NONE";
    const bypassResponsible = rule === "NO_USER";

    let assignedUserId = null;

    if (rule === "CURRENT_USER") {
      assignedUserId = this.ebauModules.userId;
    } else if (rule === "SPECIFIC_USER") {
      assignedUserId = this.selectedTemplate.get("assignedUser.id");
    }

    this.model.title = this.selectedTemplate.name;
    this.model.description = this.selectedTemplate.description;
    this.model.meta = {
      "template-id": this.selectedTemplate.id,
      "bypass-responsible-user": bypassResponsible,
    };
    this.model.deadline = DateTime.now()
      .plus({ days: this.selectedTemplate.leadTime ?? 10 })
      .toJSDate();
    this.model.addressedService = currentService
      ? this.store.peekRecord("public-service", this.args.serviceId)
      : null;
    this.model.assignedUser = assignedUserId
      ? this.store.peekRecord("public-user", assignedUserId)
      : null;
  }
}
