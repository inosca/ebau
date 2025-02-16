import { service } from "@ember/service";
import { macroCondition, getOwnConfig } from "@embroider/macros";
import CalumaOptionsService from "@projectcaluma/ember-core/services/caluma-options";
import { INQUIRY_STATUS } from "@projectcaluma/ember-distribution/config";
import { cantonAware } from "ember-ebau-core/decorators";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";
import fetchIfNotCached from "ember-ebau-core/utils/fetch-if-not-cached";
import { cached } from "tracked-toolbox";

export default class CustomCalumaOptionsService extends CalumaOptionsService {
  @service ebauModules;
  @service session;
  @service store;
  @service fetch;

  useNumberSeparatorWidgetAsDefault = hasFeature(
    "caluma.useNumberSeparatorWidgetAsDefault",
  );

  get currentGroupId() {
    return this.session.service?.id;
  }

  get currentInstanceId() {
    return this.ebauModules.instanceId;
  }

  get isAuthority() {
    if (!this.currentInstanceId) {
      return false;
    }

    const instance = this.store.peekRecord("instance", this.currentInstanceId);
    const authorityId = parseInt(instance?.belongsTo("activeService").id());

    return authorityId === parseInt(this.currentGroupId);
  }

  resolveUsers(identifiers) {
    return fetchIfNotCached("public-user", "username", identifiers, this.store);
  }

  resolveGroups(identifiers) {
    return fetchIfNotCached(
      "public-service",
      "service_id",
      identifiers,
      this.store,
    );
  }

  @cantonAware
  static distributionInfoQuestions = [];
  static distributionInfoQuestionsGR = [
    "inquiry-answer-situation",
    "inquiry-answer-considerations",
    "inquiry-answer-assessment",
    "inquiry-answer-ancillary-clauses",
  ];
  static distributionInfoQuestionsSO = [
    "inquiry-answer-positive-assessments",
    "inquiry-answer-negative-assessments",
    "inquiry-answer-rejection-additional-demand",
    "inquiry-answer-objections",
    "inquiry-answer-notices-for-applicant",
    "inquiry-answer-notices-for-authority",
    "inquiry-answer-notices-for-authority-arp",
    "inquiry-answer-forward",
  ];
  static distributionInfoQuestionsAG = ["inquiry-answer-remarks"];

  @cantonAware
  static distributionStatusMapping = {};
  static distributionStatusMappingGR = {
    "inquiry-answer-status-positive": INQUIRY_STATUS.POSITIVE,
    "inquiry-answer-status-negative": INQUIRY_STATUS.NEGATIVE,
    "inquiry-answer-status-approved": INQUIRY_STATUS.POSITIVE,
    "inquiry-answer-status-rejected": INQUIRY_STATUS.NEGATIVE,
    "inquiry-answer-status-written-off": INQUIRY_STATUS.NEGATIVE,
    "inquiry-answer-status-claim": INQUIRY_STATUS.NEEDS_INTERACTION,
    "inquiry-answer-status-not-involved": INQUIRY_STATUS.POSITIVE,
    "inquiry-answer-status-following": INQUIRY_STATUS.POSITIVE,
    "inquiry-answer-status-renounced": INQUIRY_STATUS.POSITIVE,
    "inquiry-answer-status-unknown": {
      icon: "question",
      color: "emphasis",
    },
  };
  static distributionStatusMappingSO = {
    "inquiry-answer-status-positive": INQUIRY_STATUS.POSITIVE,
    "inquiry-answer-status-negative": INQUIRY_STATUS.NEGATIVE,
    "inquiry-answer-status-additional-demand": INQUIRY_STATUS.NEEDS_INTERACTION,
    "inquiry-answer-status-rejection": INQUIRY_STATUS.NEGATIVE,
    "inquiry-answer-status-no-comment": INQUIRY_STATUS.POSITIVE,
    "inquiry-answer-status-unknown": {
      icon: "question",
      color: "emphasis",
    },
    "inquiry-answer-status-direct": {
      icon: "warning",
      color: "emphasis",
    },
  };
  static distributionStatusMappingAG = {
    "inquiry-answer-status-positive": INQUIRY_STATUS.POSITIVE,
    "inquiry-answer-status-negative": INQUIRY_STATUS.NEGATIVE,
    "inquiry-answer-status-claim": INQUIRY_STATUS.NEEDS_INTERACTION,
    "inquiry-answer-status-not-involved": INQUIRY_STATUS.POSITIVE,
  };

  @cantonAware
  get distributionServiceGroups() {
    return {};
  }

  get distributionServiceGroupsGR() {
    if (this.ebauModules.instanceId) {
      const instance = this.store.peekRecord(
        "instance",
        this.ebauModules.instanceId,
      );

      if (instance.calumaForm === "bauanzeige") {
        return {
          suggestions: { disabled: false },
          municipality: {
            label: "distribution.municipalities",
          },
          subservice: {
            label: "distribution.subservices",
          },
        };
      }

      return {
        suggestions: { disabled: false },
        "authority-bab": {
          label: "distribution.authority-bab",
        },
        service: {
          label: "distribution.services",
        },
        municipality: {
          label: "distribution.municipalities",
        },
        subservice: {
          label: "distribution.subservices",
        },
      };
    }
    return {};
  }

  get distributionServiceGroupsSO() {
    if (!this.currentInstanceId) {
      return {};
    }

    const fullConfig = {
      municipality: {
        label: "distribution.municipalities",
      },
      "service-cantonal;service-bab": {
        label: "distribution.services-cantonal",
      },
      "service-extra-cantonal": {
        label: "distribution.services-extra-cantonal",
      },
      subservice: {
        label: "distribution.subservices",
      },
    };

    if (this.session.rolePermission === "service") {
      Reflect.deleteProperty(fullConfig, "municipality");
    }

    if (!this.isAuthority) {
      fullConfig.suggestions = { disabled: true };
    }

    if (this.session.rolePermission === "municipality" && !this.isAuthority) {
      Reflect.deleteProperty(fullConfig, "municipality");
      Reflect.deleteProperty(fullConfig, "service-cantonal;service-bab");
      Reflect.deleteProperty(fullConfig, "service-extra-cantonal");
    }

    return fullConfig;
  }

  get distributionServiceGroupsAG() {
    return {
      subservice: {
        label: "distribution.subservices",
      },
      "service-cantonal;service-afb": {
        label: "distribution.services-cantonal",
      },
      "service-external": {
        label: "distribution.services-external",
      },
      municipality: {
        label: "distribution.municipalities",
      },
    };
  }

  @cantonAware
  get distributionDefaultServiceGroups() {
    return ["suggestions"];
  }

  get distributionDefaultServiceGroupsGR() {
    return [];
  }

  get distributionDefaultServiceGroupsSO() {
    if (this.isAuthority) {
      return ["suggestions"];
    }

    return ["subservice"];
  }

  @cantonAware
  static distributionButtons = {
    "fill-inquiry": {
      color: "primary",
      label: "distribution.send-answer",
      status: "caluma.distribution.answer.buttons.compose.status",
      willCompleteInquiry: true,
    },
  };

  static distributionButtonsAG = {
    "fill-inquiry": {
      color: "primary",
      label: "distribution.release-for-review",
      status: "caluma.distribution.answer.buttons.compose.status",
    },
    "check-inquiry": {
      color: "primary",
      label: "distribution.confirm",
      status: {
        label: "caluma.distribution.answer.buttons.confirm.status",
        color: { addressed: "muted", controlling: "emphasis" },
        icon: "user",
      },
      willCompleteInquiry: true,
    },
    "revise-inquiry": {
      color: "default",
      label: "distribution.revise",
    },
    "alter-inquiry": {
      color: "primary",
      label: "distribution.release-adjustment-for-review",
      status: "caluma.distribution.answer.buttons.adjust.status",
    },
  };

  @cached
  get distribution() {
    return {
      ui: {
        readonly: this.session.isReadOnlyRole,
        new: {
          showAllServices: getOwnConfig().application === "ag",
        },
      },
      inquiry: {
        answer: {
          infoQuestions: CustomCalumaOptionsService.distributionInfoQuestions,
          buttons: CustomCalumaOptionsService.distributionButtons,
          statusMapping: CustomCalumaOptionsService.distributionStatusMapping,
          ...(macroCondition(getOwnConfig().application === "ag")
            ? {
                details: (inquiry) => {
                  const releasedForReviewWorkItem =
                    inquiry.childCase.workItems.edges
                      .map((workItem) => workItem.node)
                      .filter(
                        (workItem) =>
                          ["fill-inquiry", "alter-inquiry"].includes(
                            workItem.task.slug,
                          ) && workItem.status === "COMPLETED",
                      )
                      .sort((a, b) => a.closedAt - b.closedAt)
                      .reverse()[0];

                  return [
                    {
                      label: "caluma.distribution.inquiry.sent-at",
                      value: inquiry.childCase?.createdAt,
                      type: "date",
                    },
                    {
                      label: "caluma.distribution.inquiry.assigned-user",
                      value: inquiry.assignedUsers,
                      type: "user",
                    },
                    {
                      label: "distribution.released-for-review",
                      value: releasedForReviewWorkItem?.closedAt,
                      type: "date",
                    },
                    {
                      label: "distribution.released-for-review-by",
                      value: releasedForReviewWorkItem?.closedByUser,
                      type: "user",
                    },
                    {
                      label: "caluma.distribution.inquiry.closed-at",
                      value: inquiry.closedAt,
                      type: "date",
                    },
                    {
                      label: "distribution.closed-by",
                      value: inquiry.closedByUser,
                      type: "user",
                    },
                  ];
                },
              }
            : {}),
        },
      },
      new: {
        types: this.distributionServiceGroups,
        defaultTypes: this.distributionDefaultServiceGroups,
      },
      permissions: {
        completeDistribution: () => this.session.isLeadRole,
        reopenDistribution: () => this.session.isLeadRole,
        sendInquiry: () => this.session.isLeadRole,
        withdrawInquiry: () => this.session.isLeadRole,
        completeInquiryChildWorkItem: (task) =>
          !["check-inquiry", "revise-inquiry"].includes(task) ||
          this.session.isLeadRole,
        reopenInquiry: () => this.session.isLeadRole,
        checkInquiries: () => this.session.isLeadRole,
      },
      hooks: {
        postCompleteDistribution: () => this.ebauModules.redirectToWorkItems(),
      },
      inquiryReminderNotificationTemplateSlug: "inquiry-reminder",
    };
  }

  async fetchTypedGroups(types, search) {
    return await types.reduce(async (typed, type) => {
      const filters =
        type === "subservice"
          ? { service_parent: this.ebauModules.serviceId }
          : type === "suggestions"
            ? { suggestion_for_instance: this.currentInstanceId }
            : {
                service_group_name: type.split(";").join(","),
                has_parent: false,
              };

      const result = await this.store.query("public-service", {
        search,
        exclude_own_service: true,
        available_in_distribution_for_instance: this.currentInstanceId,
        ...filters,
      });

      return { ...(await typed), [type]: result };
    }, Promise.resolve({}));
  }

  async sendReminderDistributionInquiry(inquiryId) {
    if (!this.distribution.inquiryReminderNotificationTemplateSlug) {
      return;
    }

    await this.fetch.fetch(`/api/v1/notification-templates/sendmail`, {
      method: "POST",
      headers: {
        accept: "application/vnd.api+json",
        "content-type": "application/vnd.api+json",
      },
      body: JSON.stringify({
        data: {
          type: "notification-template-sendmails",
          attributes: {
            "template-slug":
              this.distribution.inquiryReminderNotificationTemplateSlug,
            "recipient-types": ["inquiry_addressed"],
          },
          relationships: {
            instance: {
              data: { type: "instances", id: this.currentInstanceId },
            },
            inquiry: { data: { type: "work-items", id: inquiryId } },
          },
        },
      }),
    });
  }
}
