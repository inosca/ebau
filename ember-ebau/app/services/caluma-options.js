import { service } from "@ember/service";
import CalumaOptionsService from "@projectcaluma/ember-core/services/caluma-options";
import { INQUIRY_STATUS } from "@projectcaluma/ember-distribution/config";
import mainConfig from "ember-ebau-core/config/main";
import { cantonAware } from "ember-ebau-core/decorators";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";
import fetchIfNotCached from "ember-ebau-core/utils/fetch-if-not-cached";
import { DateTime } from "luxon";
import { cached } from "tracked-toolbox";
export default class CustomCalumaOptionsService extends CalumaOptionsService {
  @service emailNotification;
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
    "stellungnahme-in-dokumentanablage",
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
  static distributionInfoQuestionsAG = ["inquiry-answer-status"];
  static distributionInfoQuestionsSG = ["inquiry-answer-status"];

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
    "inquiry-answer-status-positive-sanctions": INQUIRY_STATUS.POSITIVE,
    "inquiry-answer-status-positive-partially": INQUIRY_STATUS.POSITIVE,
    "inquiry-answer-status-negative": INQUIRY_STATUS.NEGATIVE,
    "inquiry-answer-status-negative-deconstruction": INQUIRY_STATUS.NEGATIVE,
    "inquiry-answer-status-statement": { icon: "eye", color: "emphasis" },
    "inquiry-answer-status-claim": INQUIRY_STATUS.NEEDS_INTERACTION,
    "inquiry-answer-status-not-involved": { icon: "reply", color: "emphasis" },
    "inquiry-answer-status-unknown": {
      icon: "question",
      color: "emphasis",
    },
  };
  static distributionStatusMappingSG = {
    "inquiry-answer-status-positive": INQUIRY_STATUS.POSITIVE,
    "inquiry-answer-status-negative": INQUIRY_STATUS.NEGATIVE,
    "inquiry-answer-status-approved": INQUIRY_STATUS.POSITIVE,
    "inquiry-answer-status-rejected": INQUIRY_STATUS.NEGATIVE,
    "inquiry-answer-status-written-off": INQUIRY_STATUS.NEGATIVE,
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

      if (["bauanzeige", "bauanzeige-v3"].includes(instance.calumaForm)) {
        return {
          suggestions: { disabled: false },
          subservice: {
            label: "distribution.subservices",
          },
          service: {
            label: "distribution.services",
          },
          municipality: {
            label: "distribution.municipalities",
          },
        };
      }

      return {
        suggestions: { disabled: false },
        subservice: {
          label: "distribution.subservices",
        },
        "authority-bab": {
          label: "distribution.authority-bab",
        },
        service: {
          label: "distribution.services",
        },
        municipality: {
          label: "distribution.municipalities",
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

  get distributionServiceGroupsSG() {
    return {
      subservice: { label: "distribution.own-subservices" },
      coordination: { label: "distribution.coordination-service" },
      "service-cantonal?distribution-group=bud": { label: "distribution.bud" },
      "service-cantonal?distribution-group=di": { label: "distribution.di" },
      "service-cantonal?distribution-group=gd": { label: "distribution.gd" },
      "service-cantonal?distribution-group=sjd": { label: "distribution.sjd" },
      "service-external": { label: "distribution.services-external" },
      "service-federal": { label: "distribution.services-federal" },
      municipality: { label: "distribution.municipalities" },
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

  get distributionButtons() {
    if (hasFeature("distribution.fourEyesPrinciple")) {
      // Copied from SZ logic in ember-camac-ng/app/services/caluma-options.js
      return {
        "fill-inquiry": {
          color: "primary",
          label: "distribution.release-for-review",
          status: "caluma.distribution.answer.buttons.compose.status",
        },
        "check-inquiry": {
          color: "primary",
          label: "distribution.confirm",
          // Having this work item ready triggers a custom status so the user is
          // aware that the inquiry needs to be confirmed.
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
    }

    return {
      "fill-inquiry": {
        color: "primary",
        label: "distribution.send-answer",
        status: "caluma.distribution.answer.buttons.compose.status",
        willCompleteInquiry: true,
      },
    };
  }

  @cantonAware
  static distributionDefaultLeadTime = 30;
  static distributionDefaultLeadTimeAG = 14;
  static distributionDefaultLeadTimeGR = 14;

  get distributionDetails() {
    if (!hasFeature("distribution.fourEyesPrinciple")) {
      return null;
    }

    return (inquiry) => {
      // Copied from SZ logic in ember-camac-ng/app/services/caluma-options.js
      const releasedForReviewWorkItem = inquiry.childCase.workItems.edges
        .map((workItem) => workItem.node)
        .filter(
          (workItem) =>
            ["fill-inquiry", "alter-inquiry"].includes(workItem.task.slug) &&
            workItem.status === "COMPLETED",
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
    };
  }

  @cached
  get distribution() {
    const detailsFn = this.distributionDetails;

    return {
      ui: {
        readonly: this.session.isReadOnlyRole,
        new: {
          showAllServices: hasFeature("distribution.showAllServices"),
        },
      },
      inquiry: {
        answer: {
          infoQuestions: CustomCalumaOptionsService.distributionInfoQuestions,
          buttons: this.distributionButtons,
          statusMapping: CustomCalumaOptionsService.distributionStatusMapping,
          ...(detailsFn ? { details: detailsFn } : {}),
        },
      },
      new: {
        types: this.distributionServiceGroups,
        defaultTypes: this.distributionDefaultServiceGroups,
        defaultDeadlineLeadTime:
          CustomCalumaOptionsService.distributionDefaultLeadTime,
      },
      permissions: {
        completeDistribution: () => this.session.isLeadRole,
        reopenDistribution: () => this.session.isLeadRole,
        sendInquiry: () => this.session.isLeadRole,
        withdrawInquiry: () => this.session.isLeadRole,
        completeInquiryChildWorkItem: () => this.session.isLeadRole,
        reopenInquiry: () => this.session.isLeadRole,
        checkInquiries: () => this.session.isLeadRole,
      },
      hooks: {
        postCompleteDistribution: () =>
          this.ebauModules.redirectToCaseWorkItems(),
      },
      inquiryReminderNotificationTemplateSlug: "inquiry-reminder",
    };
  }

  #getGroupFilters(type) {
    if (type === "subservice") {
      return { service_parent: this.ebauModules.serviceId };
    } else if (type === "suggestions") {
      return { suggestion_for_instance: this.currentInstanceId };
    } else if (type.includes("?")) {
      const [serviceGroup, metaQuery] = type.split("?");
      const [key, value] = metaQuery.split("=");

      return {
        service_group_name: serviceGroup,
        meta: JSON.stringify({ key, value }),
        has_parent: false,
      };
    }

    return {
      service_group_name: type.split(";").join(","),
      has_parent: false,
    };
  }

  async fetchTypedGroups(types, search) {
    return await types.reduce(async (typed, type) => {
      const result = await this.store.query("public-service", {
        search,
        exclude_own_service: true,
        available_in_distribution_for_instance: this.currentInstanceId,
        ...this.#getGroupFilters(type),
      });

      return { ...(await typed), [type]: result };
    }, Promise.resolve({}));
  }

  async sendReminderDistributionInquiry(inquiryId) {
    if (!this.distribution.inquiryReminderNotificationTemplateSlug) {
      return;
    }

    await this.emailNotification.send(
      this.currentInstanceId,
      this.distribution.inquiryReminderNotificationTemplateSlug,
      ["inquiry_addressed"],
      {
        inquiry: { data: { type: "work-items", id: inquiryId } },
      },
    );
  }

  async calculateDistributionDefaultDeadline(defaultLeadTime, selectedGroups) {
    const defaultDeadline = super.calculateDistributionDefaultDeadline(
      defaultLeadTime,
      selectedGroups,
    );

    if (!hasFeature("distribution.deadlineRules")) {
      const customServiceGroupDeadline =
        mainConfig.customDeadlineServiceGroupDefaultDeadline ?? null;

      // if there is a config to override the default deadline for specific service groups,
      // check if any of the selected groups is included and return the corresponding deadline.
      // when multiple groups are selected, we ignore this behavior.
      if (customServiceGroupDeadline && selectedGroups.length === 1) {
        const customServiceGroupSlugs =
          mainConfig.customDeadlineServiceGroupSlugs ?? [];

        const selectedPublicServices = await this.store.query(
          "public-service",
          {
            filter: {
              service_id: selectedGroups.join(","),
            },
            include: "service_group",
          },
        );

        const selectedServiceGroups = (
          await Promise.all(
            selectedPublicServices.map(
              (publicService) => publicService?.serviceGroup,
            ),
          )
        )
          .filter(Boolean)
          .map((serviceGroup) => serviceGroup.slug);

        // find any selected group included in the deadline overrides.
        const includedSpecialServiceGroup = selectedServiceGroups.find((slug) =>
          customServiceGroupSlugs.includes(slug),
        );

        // when found, recalculate the deadline with the override.
        if (
          includedSpecialServiceGroup &&
          customServiceGroupDeadline[includedSpecialServiceGroup]
        ) {
          return DateTime.now()
            .plus({
              days: customServiceGroupDeadline[includedSpecialServiceGroup],
            })
            .toISODate();
        }
      }

      return defaultDeadline;
    }

    const rules = await this.store.query("distribution-deadline-rule", {
      target_service: selectedGroups.join(","),
    });

    const deadlines = [
      ...new Set([
        ...rules.map((rule) => rule.deadline),
        ...(selectedGroups.length !== rules.length ? [defaultDeadline] : []),
      ]),
    ];

    if (deadlines.length === 1) {
      return deadlines[0];
    }

    return "0000-01-01";
  }
}
