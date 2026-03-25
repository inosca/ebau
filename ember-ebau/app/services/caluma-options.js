import { service } from "@ember/service";
import { getOwnConfig } from "@embroider/macros";
import CalumaOptionsService from "@projectcaluma/ember-core/services/caluma-options";
import { INQUIRY_STATUS } from "@projectcaluma/ember-distribution/config";
import mainConfig from "ember-ebau-core/config/main";
import { cantonAware } from "ember-ebau-core/decorators";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";
import fetchIfNotCached from "ember-ebau-core/utils/fetch-if-not-cached";
import { DateTime } from "luxon";
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

  static distributionButtons = {
    "fill-inquiry": {
      color: "primary",
      label: "distribution.send-answer",
      status: "caluma.distribution.answer.buttons.compose.status",
      willCompleteInquiry: true,
    },
  };

  @cantonAware
  static distributionDefaultLeadTime = 30;
  static distributionDefaultLeadTimeAG = 14;

  @cached
  get distribution() {
    return {
      ui: {
        readonly: this.session.isReadOnlyRole,
        new: {
          showAllServices: ["ag", "gr"].includes(getOwnConfig().application),
        },
      },
      inquiry: {
        answer: {
          infoQuestions: CustomCalumaOptionsService.distributionInfoQuestions,
          buttons: CustomCalumaOptionsService.distributionButtons,
          statusMapping: CustomCalumaOptionsService.distributionStatusMapping,
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
      if (customServiceGroupDeadline) {
        const customServiceGroupSlugs =
          mainConfig.customDeadlineServiceGroupSlugs ?? [];
        const selectedServiceGroups = await Promise.all(
          selectedGroups
            .map(async (serviceGroup) => {
              return await this.store.peekRecord("public-service", serviceGroup)
                ?.serviceGroup;
            })
            .filter(Boolean),
        );

        // find any selected group included in the deadline overrides.
        const includedSpecialService = selectedServiceGroups.find(
          (sg) => sg && customServiceGroupSlugs.includes(sg.slug),
        );

        // when found, recalculate the deadline with the override.
        if (
          includedSpecialService &&
          customServiceGroupDeadline[includedSpecialService.slug]
        ) {
          return DateTime.now()
            .plus({
              days: customServiceGroupDeadline[includedSpecialService.slug],
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
