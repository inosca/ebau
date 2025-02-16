import { getOwner, setOwner } from "@ember/application";
import { service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import WorkItemModel from "@projectcaluma/ember-core/caluma-query/models/work-item";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";
import { queryManager } from "ember-apollo-client";

import CustomCaseModel from "ember-ebau-core/caluma-query/models/case";
import mainConfig from "ember-ebau-core/config/main";
import saveWorkItemMutation from "ember-ebau-core/gql/mutations/save-workitem.graphql";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";
import { getAnswerDisplayValue } from "ember-ebau-core/utils/get-answer";
import { getApplicants } from "ember-ebau-core/utils/get-applicants";

const QUESTIONS = JSON.stringify([
  ...mainConfig.intentSlugs,
  mainConfig.answerSlugs.municipality
    ? mainConfig.answerSlugs.municipality
    : "",
  mainConfig.answerSlugs.personalDataApplicant
    ? mainConfig.answerSlugs.personalDataApplicant
    : "",
]);

export default class CustomWorkItemModel extends WorkItemModel {
  @queryManager apollo;

  @service store;

  @service ebauModules;
  @service router;
  @service intl;
  @service notification;
  @service abilities;

  @tracked meta = this.raw.meta;
  @tracked notViewed = this.raw.meta["not-viewed"];
  @tracked assignedUsers = this.raw.assignedUsers;
  @tracked addressedGroups = this.raw.addressedGroups;

  get assignedUser() {
    return this.store
      .peekAll("public-user")
      .find((user) => this.assignedUsers.includes(user.username));
  }

  set assignedUser(user) {
    this.assignedUsers = [user.username];
  }

  get addressedService() {
    if (!this.addressedGroups.length) return null;

    if (!parseInt(this.addressedGroups[0])) {
      return {
        name: this.intl.t(`global.${this.addressedGroups[0]}`),
        id: this.addressedGroups[0],
      };
    }

    return this.store
      .peekAll(this.ebauModules.storeServiceName)
      .find((service) => this.addressedGroups.includes(service.id));
  }

  get closedByUser() {
    return this.store
      .peekAll("public-user")
      .find((user) => user.username === this.raw.closedByUser);
  }

  get createdByUser() {
    return this.store
      .peekAll("public-user")
      .find((user) => user.username === this.raw.closedByUser);
  }

  get createdByGroup() {
    return (
      this.raw.createdByGroup &&
      this.store.peekRecord(
        this.ebauModules.storeServiceName,
        this.raw.createdByGroup,
      )
    );
  }

  get isAddressedToCurrentService() {
    return parseInt(this.addressedService?.id) === this.ebauModules.serviceId;
  }

  get isAssignedToCurrentUser() {
    return this.assignedUsers.includes(this.ebauModules.username);
  }

  get isCreatedByCurrentService() {
    return parseInt(this.createdByGroup?.id) === this.ebauModules.serviceId;
  }

  get isControlledByCurrentService() {
    return parseInt(this.controllingGroups[0]) === this.ebauModules.serviceId;
  }

  get isReady() {
    return this.raw.status === "READY";
  }

  get isCompleted() {
    return this.raw.status === "COMPLETED";
  }

  get isCanceled() {
    return this.raw.status === "CANCELED";
  }

  get isCalumaBackend() {
    return mainConfig.name === "sz"
      ? this.case?.meta["form-backend"] === "caluma"
      : true;
  }

  get responsible() {
    if (this.isAddressedToCurrentService) {
      return this.assignedUser?.fullName || "-";
    }

    return [
      this.addressedService?.name,
      this.assignedUser ? `(${this.assignedUser.fullName})` : "",
    ]
      .filter(Boolean)
      .join(" ");
  }

  get case() {
    return this.raw.case.family;
  }

  get instanceId() {
    return this.case?.meta["camac-instance-id"];
  }

  get instance() {
    return this.store.peekRecord("instance", this.instanceId);
  }

  get instanceName() {
    const name = this.isCalumaBackend
      ? this.case?.document.form.name
      : this.instance?.name || this.instance?.form.get("description");
    const specialId =
      this.case?.meta[mainConfig.answerSlugs.specialId] ||
      this.instance?.identifier;
    const suffix = specialId ? `(${specialId})` : "";
    if (name) {
      const prefix = mainConfig.showInstanceIdAfterSubmission
        ? `${this.instanceId} - `
        : "";
      return `${prefix}${name} ${suffix}`.trim();
    }

    return this.instanceId;
  }

  get instanceDescription() {
    if (!this.isCalumaBackend) {
      const formFields = this.store
        .peekAll("form-field")
        .filter(
          (field) => field.instance.get("id") === this.instanceId.toString(),
        );

      const formField =
        formFields.find((field) => field.name === "bezeichnung-override") ||
        formFields.find((field) => field.name === "bezeichnung");

      return formField?.value;
    }

    return this.case?.document.answers.edges
      .map((edge) =>
        mainConfig.intentSlugs.includes(edge.node.question.slug)
          ? edge.node.stringValue
          : null,
      )
      .filter(Boolean)
      .join("\n");
  }

  get municipality() {
    return getAnswerDisplayValue(
      this.case.document,
      mainConfig.answerSlugs.municipality,
    );
  }

  get applicants() {
    return getApplicants(this.case.document);
  }

  get childCase() {
    const childCase = new CustomCaseModel(this.raw.childCase);
    setOwner(childCase, getOwner(this));

    return childCase;
  }

  replacePlaceholders(models) {
    let map = {
      INSTANCE_ID: this.instanceId,
      TASK_SLUG: this.task.slug,
    };

    const distributionWorkItem = [
      this.raw,
      this.raw.case.parentWorkItem,
      this.raw.case.parentWorkItem?.case.parentWorkItem,
    ]
      .filter(Boolean)
      .find((workItem) => workItem.task.slug === "distribution");

    const inquiryWorkItem = [this.raw, this.raw.case.parentWorkItem]
      .filter(Boolean)
      .find((workItem) => workItem.task.slug === "inquiry");

    const constructionStepWorkItem = [this.raw, this.raw.case.parentWorkItem]
      .filter(Boolean)
      .find((workItem) => workItem.meta["construction-step-id"]);

    if (distributionWorkItem) {
      map = {
        ...map,
        DISTRIBUTION_CASE_UUID: decodeId(distributionWorkItem.childCase.id),
      };
    }

    if (inquiryWorkItem) {
      map = {
        ...map,
        INQUIRY_UUID: decodeId(inquiryWorkItem.id),
        INQUIRY_ADDRESSED: inquiryWorkItem.addressedGroups[0],
        INQUIRY_CONTROLLING: inquiryWorkItem.controllingGroups[0],
      };
    }

    if (constructionStepWorkItem) {
      map = {
        ...map,
        CONSTRUCTION_STAGE_UUID: decodeId(
          constructionStepWorkItem.case.parentWorkItem.id,
        ),
        CONSTRUCTION_STEP_ID:
          constructionStepWorkItem.meta["construction-step-id"],
      };
    }

    return models.map((placeholder) => map[placeholder] || placeholder);
  }

  get directLink() {
    return this._getDirectLinkFor(this.raw.task.slug) ?? this.editLink;
  }

  get editLink() {
    if (this.ebauModules.isLegacyApp) {
      const url = this._getDirectLinkFor("edit");
      const hash = this.router.urlFor(
        "work-items.instance.edit",
        this.instanceId,
        this.id,
      );

      return url && `${url}${hash}`;
    }

    return {
      route: "cases.detail.work-items.edit",
      models: [this.instanceId, this.id],
    };
  }

  // TODO: Consider moving this logic to the backend, so that we don't have
  // to always fetch parent work items.
  _getLinkPlaceholders() {
    const inquiryWorkItem = [this.raw, this.raw.case.parentWorkItem]
      .filter(Boolean)
      .find((workItem) => workItem.task.slug === "inquiry");

    if (inquiryWorkItem) {
      return {
        INQUIRY_UUID: decodeId(inquiryWorkItem.id),
        INQUIRY_ADDRESSED: inquiryWorkItem.addressedGroups[0],
        INQUIRY_CONTROLLING: inquiryWorkItem.controllingGroups[0],
        DISTRIBUTION_CASE_UUID: decodeId(inquiryWorkItem.case.id),
      };
    }

    const constructionStepWorkItem = [this.raw, this.raw.case.parentWorkItem]
      .filter(Boolean)
      .find((workItem) => workItem.meta?.["construction-step-id"]);

    if (constructionStepWorkItem) {
      return {
        CONSTRUCTION_STAGE_UUID: decodeId(
          constructionStepWorkItem.case.parentWorkItem.id,
        ),
        CONSTRUCTION_STEP_ID:
          constructionStepWorkItem.meta["construction-step-id"],
      };
    }

    return {};
  }

  _getDirectLinkFor(configKey) {
    if (!this.abilities.can("edit work-item", this)) {
      return null;
    }

    // Only the addressed group should have a direct link if the work item is
    // not a manual work item
    if (
      !this.raw.addressedGroups
        .map(String)
        .includes(String(this.ebauModules.serviceId)) &&
      this.raw.task.slug !== "create-manual-workitems"
    ) {
      return null;
    }

    if (this.ebauModules.isLegacyApp) {
      const query = this.ebauModules.directLinkConfig[configKey];

      return query
        ? Object.entries(this._getLinkPlaceholders()).reduce(
            (url, [key, value]) => url.replace(`{{${key}}}`, value),
            `/index/redirect-to-instance-resource/instance-id/${this.instanceId}?${query}`,
          )
        : null;
    }

    const directLinkConfig = this.raw.task.meta.directLink;
    return directLinkConfig
      ? {
          route: directLinkConfig.route,
          models: this.replacePlaceholders(directLinkConfig.models),
        }
      : this.editLink;
  }

  async toggleRead() {
    try {
      this.notViewed = !this.notViewed;

      await this.apollo.mutate({
        mutation: saveWorkItemMutation,
        variables: {
          input: {
            workItem: this.id,
            meta: JSON.stringify({
              ...this.raw.meta,
              "not-viewed": this.notViewed,
            }),
          },
        },
      });

      return true;
    } catch {
      this.notification.danger(this.intl.t("workItems.saveError"));
    }
  }

  async assignToMe() {
    const id = this.ebauModules.userId;
    const user =
      (await this.store.peekRecord("public-user", id)) ||
      (await this.store.findRecord("public-user", id, { reload: true }));

    return await this.assignToUser(user);
  }

  async assignToUser(user) {
    try {
      this.assignedUser = user;

      await this.apollo.mutate({
        mutation: saveWorkItemMutation,
        variables: {
          input: {
            workItem: this.id,
            assignedUsers: this.assignedUsers,
          },
        },
      });

      return true;
    } catch {
      this.notification.danger(this.intl.t("workItems.saveError"));
    }
  }

  static fragment = `{
    createdAt
    createdByUser
    createdByGroup
    closedAt
    closedByUser
    closedByGroup
    status
    meta
    addressedGroups
    controllingGroups
    assignedUsers
    name
    deadline
    description
    task {
      slug
      meta
    }
    ${hasFeature("workItems.showDocument") ? "document { id }" : ""}
    case {
      id
      meta
      family {
        id
        meta
        document {
          id
          form {
            name
          }
          answers(filter: [{ questions: ${QUESTIONS} }]) {
            edges {
              node {
                question {
                  id
                  slug
                  ... on TableQuestion {
                    rowForm {
                      slug
                    }
                  }
                }
                ... on TableAnswer {
                  value {
                    answers {
                      edges {
                        node {
                          question {
                            slug
                          }
                          ... on StringAnswer {
                            stringValue: value
                          }
                        }
                      }
                    }
                  }
                }
                ... on StringAnswer {
                  stringValue: value
                  selectedOption {
                    slug
                    label
                  }
                }
              }
            }
          }
        }
      }
      parentWorkItem {
        id
        meta
        addressedGroups
        controllingGroups
        task {
          slug
          meta
        }
        case {
          id
        }
        childCase {
          id
        }
      }
    }
  }
  `;
}
